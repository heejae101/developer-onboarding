"""
Enhanced Agent Nodes - Self-RAG, 병렬검색, Answer Grading 패턴 노드
"""
from src.agent.state import AgentState
from src.llm import get_llm_client
from src.graph_settings import get_graph_settings
import json
import asyncio


# ============================================================
# Self-RAG 패턴 노드
# ============================================================

async def evaluate_node(state: AgentState) -> AgentState:
    """
    RAG 결과의 관련성과 충분성을 평가하는 노드
    - 관련성이 낮으면 재검색 트리거
    """
    settings = get_graph_settings()
    llm = get_llm_client()
    
    rag_results = state.get("rag_results", [])
    message = state.get("message", "")
    
    if not rag_results:
        # 결과가 없으면 재검색 필요
        state["is_relevant"] = False
        state["relevance_score"] = 0.0
        return state
    
    # LLM으로 관련성 평가
    context = "\n".join([r.get("content", "") for r in rag_results[:3]])
    
    prompt = f"""다음 검색 결과가 사용자 질문에 충분히 관련이 있는지 평가하세요.

[사용자 질문]
{message}

[검색 결과]
{context[:2000]}

JSON 형식으로 응답:
{{
    "relevance_score": 0.0~1.0 (관련성 점수),
    "is_sufficient": true/false (답변하기에 충분한지),
    "reason": "평가 이유",
    "suggested_query": "더 좋은 검색 쿼리 (필요시)"
}}"""

    response = llm.chat([
        {"role": "system", "content": "You are a relevance evaluator. Respond only with JSON."},
        {"role": "user", "content": prompt}
    ])
    
    try:
        content = _extract_content(response)
        result = json.loads(content)
        
        state["relevance_score"] = result.get("relevance_score", 0.5)
        state["is_relevant"] = (
            result.get("is_sufficient", True) and 
            state["relevance_score"] >= settings.relevance_threshold
        )
        
        # 재검색이 필요하면 쿼리 수정
        if not state["is_relevant"] and result.get("suggested_query"):
            state["search_query"] = result["suggested_query"]
            
    except (json.JSONDecodeError, KeyError):
        state["is_relevant"] = True  # 파싱 실패 시 진행
        state["relevance_score"] = 0.5
    
    if settings.enable_step_logging:
        print(f"📊 [Evaluate] relevance={state['relevance_score']:.2f}, relevant={state['is_relevant']}")
    
    return state


def should_retry_search(state: AgentState) -> str:
    """Self-RAG: 재검색 여부 결정"""
    settings = get_graph_settings()
    
    attempts = state.get("search_attempts", 0)
    is_relevant = state.get("is_relevant", True)
    
    if not is_relevant and attempts < settings.max_search_retries:
        return "retry"
    return "continue"


# ============================================================
# 병렬 검색 패턴 노드
# ============================================================

async def parallel_search_node(state: AgentState) -> AgentState:
    """
    RAG + 파일검색을 병렬로 실행하는 노드
    """
    from src.agent.tools import RuleSearchTool, FileSearchTool
    
    settings = get_graph_settings()
    message = state.get("message", "")
    search_query = state.get("search_query", message)
    
    # 검색 시도 횟수 증가
    state["search_attempts"] = state.get("search_attempts", 0) + 1
    
    def search_rag():
        tool = RuleSearchTool()
        result = tool.search(search_query)
        return {"source": "rag", "content": result}
    
    def search_files():
        tool = FileSearchTool()
        results = tool.search_files(search_query)
        return {"source": "file", "results": results}
    
    # 병렬 실행
    if settings.enable_parallel_search:
        rag_task = asyncio.create_task(asyncio.to_thread(search_rag))
        file_task = asyncio.create_task(asyncio.to_thread(search_files))
        
        rag_result, file_result = await asyncio.gather(rag_task, file_task)
    else:
        rag_result = await asyncio.to_thread(search_rag)
        file_result = {"source": "file", "results": []}
    
    state["rag_results"] = [rag_result] if rag_result else []
    state["file_results"] = file_result.get("results", [])
    
    if settings.enable_step_logging:
        print(f"🔍 [Search] RAG={len(state['rag_results'])}, Files={len(state['file_results'])}")
    
    return state


async def synthesize_node(state: AgentState) -> AgentState:
    """
    여러 소스의 검색 결과를 통합하여 컨텍스트 생성
    """
    settings = get_graph_settings()
    llm = get_llm_client()
    
    rag_results = state.get("rag_results", [])
    file_results = state.get("file_results", [])
    message = state.get("message", "")
    
    # RAG 결과 추출
    rag_context = ""
    for r in rag_results:
        if isinstance(r, dict):
            rag_context += r.get("content", "") + "\n"
    
    # 파일 결과 포맷
    file_context = ""
    if file_results:
        file_context = "관련 파일:\n" + "\n".join([
            f"- {f.get('name', '')} ({f.get('path', '')})" 
            for f in file_results[:5]
        ])
    
    # LLM으로 통합 응답 생성
    prompt = f"""사용자 질문에 대해 검색된 정보를 바탕으로 답변하세요.

[질문]
{message}

[프로젝트 규칙/문서]
{rag_context[:3000]}

[관련 파일]
{file_context}

위 정보를 종합하여 친절하고 정확하게 답변해주세요."""

    response = llm.chat([
        {"role": "system", "content": "You are a helpful developer assistant."},
        {"role": "user", "content": prompt}
    ])
    
    content = _extract_content(response)
    state["final_response"] = content
    state["combined_context"] = rag_context + "\n" + file_context
    
    if settings.enable_step_logging:
        print(f"📝 [Synthesize] Generated response ({len(content)} chars)")
    
    return state


# ============================================================
# Answer Grading 패턴 노드
# ============================================================

async def grade_answer_node(state: AgentState) -> AgentState:
    """
    생성된 답변의 품질을 평가하는 노드
    """
    settings = get_graph_settings()
    llm = get_llm_client()
    
    answer = state.get("final_response", "")
    message = state.get("message", "")
    context = state.get("combined_context", "")
    
    prompt = f"""생성된 답변의 품질을 평가하세요.

[사용자 질문]
{message}

[참조 컨텍스트]
{context[:1500]}

[생성된 답변]
{answer}

다음 기준으로 평가하고 JSON으로 응답:
1. 정확성: 컨텍스트 기반으로 정확한가?
2. 완전성: 질문에 충분히 답변했는가?
3. 명확성: 이해하기 쉬운가?

{{
    "score": 0.0~1.0,
    "is_acceptable": true/false,
    "feedback": "개선이 필요한 점",
    "missing_info": ["빠진 정보 목록"]
}}"""

    response = llm.chat([
        {"role": "system", "content": "You are a quality evaluator. Respond only with JSON."},
        {"role": "user", "content": prompt}
    ])
    
    try:
        content = _extract_content(response)
        result = json.loads(content)
        
        state["answer_score"] = result.get("score", 0.7)
        state["grading_feedback"] = result.get("feedback", "")
        
    except (json.JSONDecodeError, KeyError):
        state["answer_score"] = 0.75  # 파싱 실패 시 통과
        state["grading_feedback"] = ""
    
    if settings.enable_step_logging:
        print(f"⭐ [Grade] score={state['answer_score']:.2f}")
    
    return state


def should_refine_answer(state: AgentState) -> str:
    """Answer Grading: 답변 개선 여부 결정"""
    settings = get_graph_settings()
    
    score = state.get("answer_score", 1.0)
    attempts = state.get("refine_attempts", 0)
    
    if score < settings.min_answer_score and attempts < settings.max_refine_attempts:
        return "refine"
    return "complete"


async def refine_answer_node(state: AgentState) -> AgentState:
    """
    품질이 낮은 답변을 개선하는 노드
    """
    settings = get_graph_settings()
    llm = get_llm_client()
    
    state["refine_attempts"] = state.get("refine_attempts", 0) + 1
    
    answer = state.get("final_response", "")
    feedback = state.get("grading_feedback", "")
    message = state.get("message", "")
    context = state.get("combined_context", "")
    
    prompt = f"""답변을 개선하세요.

[사용자 질문]
{message}

[현재 답변]
{answer}

[개선 피드백]
{feedback}

[참조 컨텍스트]
{context[:1500]}

피드백을 반영하여 더 나은 답변을 작성하세요."""

    response = llm.chat([
        {"role": "system", "content": "You are a helpful assistant improving your previous answer."},
        {"role": "user", "content": prompt}
    ])
    
    content = _extract_content(response)
    state["final_response"] = content
    
    if settings.enable_step_logging:
        print(f"🔄 [Refine] Attempt {state['refine_attempts']}")
    
    return state


# ============================================================
# 유틸리티 함수
# ============================================================

def _extract_content(response) -> str:
    """다양한 LLM 응답 형식에서 컨텐츠 추출"""
    try:
        if hasattr(response, 'choices'):  # OpenAI
            return response.choices[0].message.content
        elif hasattr(response, 'content'):  # Anthropic
            if isinstance(response.content, list):
                return response.content[0].text
            return response.content
        elif isinstance(response, dict):  # Ollama
            return response.get("message", {}).get("content", str(response))
        else:
            return str(response)
    except (AttributeError, IndexError, KeyError):
        return str(response)
