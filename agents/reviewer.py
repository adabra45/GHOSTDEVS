"""
Code Reviewer agent - Now does real code review
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graphs.state import GhostState
from config.prompts import REVIEWER_PROMPT
from agents.base import get_llm


def reviewer_node(state: GhostState) -> dict:
    llm = get_llm("worker")

    # Collect recent code + test messages
    recent_content = ""
    for msg in state.get("messages", [])[-6:]:
        recent_content += msg.content + "\n\n"

    messages = [
        SystemMessage(content=REVIEWER_PROMPT),
        HumanMessage(content=f"""
User Request: {state.get('original_request')}

Here is the recent work from the team (code + tests):
{recent_content}

Please do a proper code review:
- Is the code correct?
- Are there any bugs or edge cases missing?
- Is the code clean and readable?
- Any improvements you suggest?
- Final verdict: Approve or Request changes
""")
    ]

    response = llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.content)],
        "status": "reviewing",
    }