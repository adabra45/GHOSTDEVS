"""
Backend Engineer agent - Now generates real code
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graphs.state import GhostState
from config.prompts import BACKEND_ENGINEER_PROMPT
from agents.base import get_llm


def backend_engineer_node(state: GhostState) -> dict:
    llm = get_llm("worker")

    architecture = state.get("architecture") or {}
    architecture_summary = architecture.get("summary", "No architecture provided")
    task = state.get("current_task", state.get("original_request", ""))

    messages = [
        SystemMessage(content=BACKEND_ENGINEER_PROMPT),
        HumanMessage(content=f"""
User Request: {state.get('original_request')}

Architecture Summary:
{architecture_summary}

Your Task:
{task}

Please write clean, working Python code for this request.
Include the full function and a simple example of how to use it.
""")
    ]

    response = llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.content)],
        "status": "implementing",
    }