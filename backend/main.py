from langchain_nvidia import NVIDIAEmbeddings
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pprint import pprint
from syfu.core.db import init_db

init_db()

load_dotenv()

soul = open("./test/info/soul.md", "r").read()
pprint(soul)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)

# llm = ChatGroq(
#     model="gemini-3.5-flash",
#     temperature=0,
# )

# llm = ChatOpenAI(
#     model="big-pickle",
#     openai_api_key=os.getenv("OPENCODE_API_KEY"),
#     openai_api_base="https://opencode.ai/zen/v1",
#     temperature=0
# )
embedding = NVIDIAEmbeddings(model="nvidia/nemotron-3-embed-1b")

pprint(llm.invoke(f"{soul}\nhelllo").content)

from syfu.tools.tasks import *
from syfu.tools.web_research import *

tools = [
    create_tasks,
    get_tasks,
    get_task_by_id,
    get_tasks_by_title,
    delete_tasks,
    complete_task,
    update_tasks,
    web_search,
    deep_search
]
tos = {t.name: t for t in tools}

llm = llm.bind_tools(tools)

from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict
from syfu.prompts.system_prompts import main_prompt
import json, inspect
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

async def _execute_tool(tool, args):
    """Executes a tool using ainvoke if async, otherwise invoke."""
    is_async = (
        getattr(tool, "coroutine", None) is not None
        or getattr(tool, "is_async", False)
        or inspect.iscoroutinefunction(getattr(tool, "func", None))
    )
    
    if is_async:
        return await tool.ainvoke(args)
    return tool.invoke(args)

async def tool_node(state: dict):
    """
    This calls the given tools.
    """
    res = []
    for m in state["messages"]:
        print("[tool_node]", m)
    print()
    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == "create_tasks":
            task = await _execute_tool(
                get_tasks_by_title,
                {"title": [x["title"] for x in tool_call["args"]["tasks"]]}
            )
            if task:
                msg = ToolMessage(content=f"{task}", tool_call_id=tool_call["id"])
                print("[tool_node][create_task][found]", msg)
                if msg.content != "[]":
                    res.append(msg)
                    continue
        call = tos[tool_call["name"]]
        ivk = await _execute_tool(call, tool_call["args"])
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


agent_builder = StateGraph(MessageState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")

agent = agent_builder.compile()

import asyncio
messages = [HumanMessage(content=input("Enter your research query: "))]

async def main():
    result = await agent.ainvoke({'messages': messages})
    
    # 2. Extract the 'messages' list from the returned state dictionary
    for msg in result['messages']:
        print(msg.content)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())
