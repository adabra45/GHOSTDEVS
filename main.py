"""
GHOSTDEVS – Entry point
"""

from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from langchain_core.messages import HumanMessage

from graphs.main_graph import graph

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]GHOSTDEVS[/bold cyan]\n"
        "Autonomous Multi-Agent Software Engineering Team",
        title="Welcome",
        border_style="cyan"
    ))

    # Simple test run
    user_request = input("\nWhat feature would you like me to build? → ")

    initial_state = {
        "messages": [HumanMessage(content=user_request)],
        "original_request": user_request,
        "current_task": None,
        "next_agent": "supervisor",
        "routing_reason": "",
        "plan": None,
        "architecture": None,
        "code_changes": [],
        "test_results": None,
        "review_feedback": None,
        "iteration_count": 0,
        "max_iterations": 15,
        "human_approved": False,
        "status": "planning",
        "final_summary": None,
        "pr_description": None,
    }

    config = {"configurable": {"thread_id": "ghostdevs-test-1"}}

    console.print("\n[bold yellow]Starting GHOSTDEVS...[/bold yellow]\n")

    for event in graph.stream(initial_state, config, stream_mode="values"):
        if "messages" in event and event["messages"]:
            last_msg = event["messages"][-1]
            console.print(f"[bold]{last_msg.type.upper()}:[/bold] {last_msg.content[:500]}")
            console.print("-" * 60)

    console.print("\n[bold green]Run finished![/bold green]")


if __name__ == "__main__":
    main()