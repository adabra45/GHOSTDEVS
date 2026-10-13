"""
Supervisor agent – Forced sequential flow (better for local models)
"""

from langchain_core.messages import AIMessage
from langgraph.types import Command
from langgraph.graph import END
from graphs.state import GhostState


def supervisor_node(state: GhostState) -> Command:
    iteration = state.get("iteration_count", 0)
    max_iter = state.get("max_iterations", 12)

    # Hard stop
    if iteration >= max_iter:
        return Command(
            goto=END,
            update={
                "status": "failed",
                "final_summary": "Max iterations reached.",
                "messages": [AIMessage(content="Stopped due to max iterations.")]
            }
        )

    # ==============================
    # FORCED SEQUENTIAL FLOW
    # ==============================

    if iteration == 0:
        next_agent = "architect"
        task = "Analyze the user request and propose a clean architecture / design."
    
    elif iteration == 1:
        next_agent = "backend_engineer"
        task = "Implement the code based on the architecture. Write clean, working Python code."
    
    elif iteration == 2:
        next_agent = "tester"
        task = "Review the code and write test cases. Check for edge cases."
    
    elif iteration == 3:
        next_agent = "reviewer"
        task = "Do a final code review. Check quality, correctness and suggest improvements."
    
    else:
        return Command(
            goto=END,
            update={
                "status": "completed",
                "final_summary": "Feature completed by the team.",
                "messages": [AIMessage(content="All agents have finished their work.")]
            }
        )

    return Command(
        goto=next_agent,
        update={
            "next_agent": next_agent,
            "current_task": task,
            "iteration_count": iteration + 1,
            "status": "implementing",
            "messages": [AIMessage(content=f"Supervisor → {next_agent}: {task}")]
        }
    )