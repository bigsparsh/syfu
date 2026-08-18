from langchain_nvidia import NVIDIAEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pprint import pprint
from syfu.core.db import init_db

init_db()

load_dotenv()

soul = open("./rag/test/info/soul.md", "r").read()
pprint(soul)

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

embedding = NVIDIAEmbeddings(model="nvidia/nemotron-3-embed-1b")

pprint(llm.invoke(f"{soul}\nhelllo").content)

from syfu.tools.tasks import *

tools = [create_tasks, get_tasks, get_task_by_id, get_tasks_by_title]
tos = {t.name: t for t in tools}

llm = llm.bind_tools(tools)

from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict
from syfu.prompts.system_prompts import main_prompt
import json
import operator


class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def llm_call(state: dict):
    """
    Calls the LLM with the current state.
    """
    res = llm.invoke([SystemMessage(content=main_prompt)] + state["messages"])
    for m in [res]:
        print("[llm_call]", m)
    print()
    return {"messages": [res], "llm_calls": state.get("llm_calls", 0) + 1}


def tool_node(state: dict):
    """
    This calls the given tools.
    """
    res = []
    for m in state["messages"]:
        print("[tool_node]", m)
    print()
    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == "create_tasks":
            task = get_tasks_by_title.invoke(tool_call["args"]["title"])
            if task:
                msg = ToolMessage(content=f"{task}", tool_call_id=tool_call["id"])
                print("[tool_node][create_task][found]", msg)
                if msg.content != "[]":
                    res.append(msg)
                    continue
        call = tos[tool_call["name"]]
        ivk = call.invoke(tool_call["args"])
        msg = ToolMessage(content=ivk, tool_call_id=tool_call["id"])
        print(f"[tool_node][{tool_call['name']}]", msg)
        res.append(msg)
        print()
    return {"messages": res}


def should_continue(state: dict):
    """
    Decide if the loop should continue or stop based upon whether the LLM made a tool call.
    """

    if state["messages"][-1].tool_calls:
        return "tool_node"
    return END


def rerun(state: dict):
    """
    Decide if another tool needs to be called after the previous one.
    """

    if state["messages"][-1].content[0] == "Already Exists":
        return "llm_call"
    else:
        return "tool_node"


agent_builder = StateGraph(MessageState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
# agent_builder.add_conditional_edges("tool_node", rerun, ["tool_node", "llm_call"])
agent_builder.add_edge("tool_node", "llm_call")

agent = agent_builder.compile()
#
# from IPython.display import Image, display
#
# display(Image(agent.get_graph(xray=True).draw_mermaid_png()))
#
# messages = [HumanMessage(content="I wanna get my clothes washed by tommorrow 5pm.")]
# messages = agent.invoke({"messages": messages})
#
# for m in messages["messages"]:
#     pprint(m)
