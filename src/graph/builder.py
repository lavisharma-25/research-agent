from langgraph.graph import StateGraph, START, END

from src.agents.supervisor import supervisor
from src.graph.state import AgentState
from src.graph.checkpointer import get_checkpointer


async def build_workflow(checkpointer=None):

    graph = StateGraph(AgentState)

    # -------------------
    # Nodes
    # -------------------
    graph.add_node("supervisor", supervisor)


    # -------------------
    # Edges
    # -------------------
    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", END)

    # -------------------
    # Compile with safe checkpointer
    # -------------------
    if checkpointer is None:
        checkpointer = await get_checkpointer()

    workflow = graph.compile(checkpointer=checkpointer)

    return workflow

async def get_workflow():
    checkpointer = await get_checkpointer()
    return await build_workflow(checkpointer=checkpointer)