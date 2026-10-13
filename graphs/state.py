"""
Shared state schema for GHOSTDEVS multi-agent system.
"""

from typing import Annotated, Literal, Optional, List, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
import operator


# ============================================================
# Structured Decision Models (Pydantic)
# ============================================================

class RouteDecision(BaseModel):
    """Supervisor's routing decision"""
    next_agent: Literal[
        "architect",
        "backend_engineer",
        "frontend_engineer",
        "tester",
        "reviewer",
        "devops",
        "researcher",
        "FINISH"
    ] = Field(description="Which agent should act next")
    reasoning: str = Field(description="Why this agent was chosen")
    task_description: str = Field(
        description="Clear, self-contained task for the next agent. Include all necessary context."
    )
    priority: Literal["high", "medium", "low"] = "medium"


class ArchitectureDecision(BaseModel):
    """Output from Architect agent"""
    summary: str
    proposed_structure: List[str]
    tech_choices: Dict[str, str]
    risks: List[str]
    estimated_complexity: Literal["low", "medium", "high"]


class CodeChange(BaseModel):
    """Single file change"""
    file_path: str
    action: Literal["create", "modify", "delete"]
    content: Optional[str] = None
    explanation: str


class ReviewFeedback(BaseModel):
    """Output from Code Reviewer"""
    approved: bool
    critical_issues: List[str]
    suggestions: List[str]
    security_concerns: List[str]
    overall_score: int = Field(ge=1, le=10)


# ============================================================
# Main Graph State (TypedDict)
# ============================================================

class GhostState(TypedDict):
    # Conversation history (accumulates)
    messages: Annotated[List[BaseMessage], add_messages]

    # Core task
    original_request: str
    current_task: Optional[str]

    # Routing
    next_agent: Literal[
        "architect", "backend_engineer", "frontend_engineer",
        "tester", "reviewer", "devops", "researcher", "FINISH"
    ]
    routing_reason: str

    # Shared working memory
    plan: Optional[str]
    architecture: Optional[Dict[str, Any]]
    code_changes: Annotated[List[Dict], operator.add]
    test_results: Optional[Dict[str, Any]]
    review_feedback: Optional[Dict[str, Any]]

    # Control & Safety
    iteration_count: int
    max_iterations: int
    human_approved: bool
    status: Literal[
        "planning", "implementing", "testing",
        "reviewing", "waiting_human", "completed", "failed"
    ]

    # Artifacts
    final_summary: Optional[str]
    pr_description: Optional[str]