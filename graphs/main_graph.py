"""
Main LangGraph for GHOSTDEVS
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from graphs.state import GhostState
from agents.supervisor import supervisor_node
from agents.architect import architect_node
from agents.backend_engineer import backend_engineer_node
from agents.tester import tester_node
from agents.reviewer import reviewer_node


def create_ghostdevs_graph():
    builder = StateGraph(GhostState)

    # Add only the agents that currently exist
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("architect", architect_node)
    builder.add_node("backend_engineer", backend_engineer_node)
    builder.add_node("tester", tester_node)
    builder.add_node("reviewer", reviewer_node)

    # Entry point
    builder.add_edge(START, "supervisor")

    # After specialists → go back to supervisor
    builder.add_edge("architect", "supervisor")
    builder.add_edge("backend_engineer", "supervisor")
    builder.add_edge("tester", "supervisor")
    builder.add_edge("reviewer", "supervisor")

    # Compile
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

    return graph


graph = create_ghostdevs_graph()