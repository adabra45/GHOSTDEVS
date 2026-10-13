"""
Architect agent.
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graphs.state import GhostState, ArchitectureDecision
from config.prompts import ARCHITECT_PROMPT
from agents.base import get_llm


def architect_node(state: GhostState) -> dict:
    llm = get_llm("worker")
    structured_llm = llm.with_structured_output(ArchitectureDecision)

    messages = [
        SystemMessage(content=ARCHITECT_PROMPT),
        HumanMessage(content=f"""
User request: {state.get('original_request')}
Current task given by Supervisor: {state.get('current_task')}

Please produce a clear architecture decision.
""")
    ]

    decision: ArchitectureDecision = structured_llm.invoke(messages)

    return {
        "architecture": decision.model_dump(),
        "messages": [AIMessage(content=f"Architecture proposed:\n{decision.summary}")],
        "status": "planning",
    }