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
    
    # ===== Self-RAG 패턴 =====
    search_attempts: int  # 현재 검색 시도 횟수
    relevance_score: float  # RAG 결과 관련성 점수 (0~1)
    is_relevant: bool  # 결과가 충분히 관련있는지
    search_query: str  # 현재/수정된 검색 쿼리
    
    # ===== 병렬 검색 패턴 =====
    rag_results: list[dict]  # RAG 검색 결과
    file_results: list[dict]  # 파일 검색 결과
    combined_context: str  # 통합된 컨텍스트
    
    # ===== Answer Grading 패턴 =====
    answer_score: float  # 답변 품질 점수 (0~1)
    refine_attempts: int  # 답변 개선 시도 횟수
    grading_feedback: str  # 품질 평가 피드백
    
    # Output
    final_response: str
    stream_tokens: list[str]


# Intent types for routing
IntentType = Literal["SEARCH", "VERIFY", "CODE_REVIEW", "AUTONOMOUS"]

