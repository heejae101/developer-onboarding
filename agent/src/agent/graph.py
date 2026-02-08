"""
LangGraph Dynamic Graph Builder
설정에 따라 Self-RAG, 병렬검색, Answer Grading 패턴을 동적으로 구성
"""
from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.graph_settings import get_graph_settings, GraphSettings

# 기존 노드들
from src.agent.nodes import (
    router_node,
    verify_rules_node,
    code_review_node,
    think_node,
    act_node,
    should_continue,
    complete_node,
)

# 개선된 노드들
from src.agent.enhanced_nodes import (
    evaluate_node,
    parallel_search_node,
    synthesize_node,
    grade_answer_node,
    refine_answer_node,
    should_retry_search,
    should_refine_answer,
)


def build_agent_graph(settings: GraphSettings = None) -> StateGraph:
    """
    설정에 따라 동적으로 그래프 구성
    
    패턴별 활성화:
    - enable_self_rag: search → evaluate → (retry?) → synthesize
    - enable_parallel_search: RAG + 파일 동시 검색
    - enable_answer_grading: synthesize → grade → (refine?) → complete
    """
    settings = settings or get_graph_settings()
    
    graph = StateGraph(AgentState)
    
    # ===== 기본 노드 등록 =====
    graph.add_node("router", router_node)
    graph.add_node("verify", verify_rules_node)
    graph.add_node("code_review", code_review_node)
    graph.add_node("think", think_node)
    graph.add_node("act", act_node)
    graph.add_node("complete", complete_node)
    
    # ===== Entry Point =====
    graph.set_entry_point("router")
    
    # ===== 검색 경로 구성 =====
    if settings.enable_self_rag or settings.enable_parallel_search:
        # 개선된 검색 노드 사용
        graph.add_node("search", parallel_search_node)
        graph.add_node("evaluate", evaluate_node)
        graph.add_node("synthesize", synthesize_node)
        
        if settings.enable_self_rag:
            # Self-RAG: search → evaluate → (retry or continue)
            graph.add_edge("search", "evaluate")
            graph.add_conditional_edges(
                "evaluate",
                should_retry_search,
                {
                    "retry": "search",  # 재검색
                    "continue": "synthesize",  # 충분하면 진행
                }
            )
        else:
            # Self-RAG 비활성화: 바로 synthesize
            graph.add_edge("search", "synthesize")
        
        if settings.enable_answer_grading:
            # Answer Grading 활성화
            graph.add_node("grade", grade_answer_node)
            graph.add_node("refine", refine_answer_node)
            
            graph.add_edge("synthesize", "grade")
            graph.add_conditional_edges(
                "grade",
                should_refine_answer,
                {
                    "refine": "refine",
                    "complete": "complete",
                }
            )
            graph.add_edge("refine", "grade")  # 개선 후 다시 평가
        else:
            # Answer Grading 비활성화: 바로 complete
            graph.add_edge("synthesize", "complete")
    else:
        # 기존 단순 검색 노드 사용
        from src.agent.nodes import search_rules_node
        graph.add_node("search", search_rules_node)
        graph.add_edge("search", "complete")
    
    # ===== 라우터 조건부 엣지 =====
    graph.add_conditional_edges(
        "router",
        lambda state: state.get("next_node", "search"),
        {
            "search": "search",
            "verify": "verify",
            "code_review": "code_review",
            "autonomous": "think",
            "complete": "complete",
        }
    )
    
    # ===== verify, code_review 경로 =====
    graph.add_edge("verify", "complete")
    graph.add_edge("code_review", "complete")
    
    # ===== Autonomous 루프 =====
    graph.add_edge("think", "act")
    graph.add_conditional_edges(
        "act",
        should_continue,
        {
            "continue": "think",
            "complete": "complete",
        }
    )
    
    # ===== 종료 =====
    graph.add_edge("complete", END)
    
    return graph.compile()


# ===== 싱글톤 그래프 관리 =====
_graph = None
_current_settings_hash = None


def _settings_hash(settings: GraphSettings) -> str:
    """설정의 해시값 (변경 감지용)"""
    return f"{settings.enable_self_rag}_{settings.enable_parallel_search}_{settings.enable_answer_grading}"


def get_agent_graph():
    """
    설정에 맞는 그래프 반환 (캐시됨)
    설정 변경 시 자동으로 재빌드
    """
    global _graph, _current_settings_hash
    
    settings = get_graph_settings()
    new_hash = _settings_hash(settings)
    
    if _graph is None or _current_settings_hash != new_hash:
        print("\n" + "=" * 50)
        print("[Graph] Rebuilding Agent Graph...")
        print(f"   - Self-RAG: {'ON' if settings.enable_self_rag else 'OFF'}")
        print(f"   - Parallel Search: {'ON' if settings.enable_parallel_search else 'OFF'}")
        print(f"   - Answer Grading: {'ON' if settings.enable_answer_grading else 'OFF'}")
        print("=" * 50 + "\n")
        
        _graph = build_agent_graph(settings)
        _current_settings_hash = new_hash
    
    return _graph


def invalidate_graph():
    """그래프 캐시 무효화 (설정 변경 시 호출)"""
    global _graph, _current_settings_hash
    _graph = None
    _current_settings_hash = None
    print("[Graph] Cache invalidated. Next request will rebuild graph.")
