"""
Agent State and Graph definitions for LangGraph
"""
from typing import TypedDict, Literal, Any
from langgraph.graph import StateGraph, END


class AgentState(TypedDict, total=False):
    """State definition for the agent graph"""
    
    # Input
    thread_id: str
    user_id: int
    message: str
    user_code: str | None
    
    # Routing
    next_node: Literal["search", "verify", "code_review", "autonomous", "complete"]
    
    # RAG
    retrieved_rules: list[dict]
    
    # Validation
    validation_result: dict | None
    
    # Code Review
    code_review_result: dict | None
    
    # Autonomous Agent
    task_description: str
    max_steps: int
    steps_completed: int
    completed_steps: list[dict]
    current_thought: str
    action_plan: dict | None
    action_result: str
    last_observation: str
    error: str | None
    
    # Output
    final_response: str
    stream_tokens: list[str]


# Intent types for routing
IntentType = Literal["SEARCH", "VERIFY", "CODE_REVIEW", "AUTONOMOUS"]
