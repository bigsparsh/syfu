from uuid import uuid4
import uuid
from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict
from src.background.prompts import system_prompt
import inspect
from src.background.llm import llm, tos
import operator

class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    prompt_id: uuid
    llm_calls: int


def llm_call(state: dict):
    """
    Calls the LLM with the current state.
    """
    res = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
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