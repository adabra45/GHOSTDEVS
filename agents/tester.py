"""
Tester / QA agent - Now generates real test cases
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graphs.state import GhostState
from config.prompts import TESTER_PROMPT
from agents.base import get_llm


def tester_node(state: GhostState) -> dict:
    llm = get_llm("worker")

    # Get the last message from Backend Engineer (the code)
    last_code = ""
    for msg in reversed(state.get("messages", [])):
        if "def " in msg.content or "factorial" in msg.content.lower():
            last_code = msg.content
            break

    messages = [
        SystemMessage(content=TESTER_PROMPT),
        HumanMessage(content=f"""
User Request: {state.get('original_request')}

Here is the code written by the Backend Engineer:
{last_code}

Your task:
1. Write proper unit tests for this function.
2. Include edge cases (0, 1, negative numbers, large numbers).
3. Show the test code clearly.
""")
    ]

    response = llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.content)],
        "status": "testing",
    }