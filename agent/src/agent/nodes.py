"""
Agent nodes implementation
"""
from src.agent.state import AgentState, IntentType
from src.llm import get_llm_client
import json


async def router_node(state: AgentState) -> AgentState:
    """Router node - determines intent and routes to appropriate handler"""
    from src.agent.tools import GuardrailsTool
    
    # Validate question first (Async)
    is_valid, reason = await GuardrailsTool.is_valid_question(state.get("message", ""))
    if not is_valid:
        state["final_response"] = reason + GuardrailsTool.suggest_alternative("")
        state["next_node"] = "complete"
        return state
    
    llm = get_llm_client()
    
    prompt = f"""사용자 입력을 분석하여 의도를 파악하세요.

사용자 입력: {state.get("message", "")}

다음 중 하나를 선택하세요:
- SEARCH: 단순 질문, 규칙 검색, **파일 찾기**
- VERIFY: 코드/문서가 규칙에 맞는지 검증
- CODE_REVIEW: 코드 리뷰 요청 (스타일, 버그, 성능)
- AUTONOMOUS: 복잡한 작업 (파일 생성, 다단계 분석)

JSON 형식으로 응답: {{"intent": "SEARCH" | "VERIFY" | "CODE_REVIEW" | "AUTONOMOUS"}}"""

    response = llm.chat([
        {"role": "system", "content": "You are an intent classifier. Respond only with JSON."},
        {"role": "user", "content": prompt}
    ])
    
    try:
        if hasattr(response, 'choices'):
            content = response.choices[0].message.content
        elif hasattr(response, 'content'):
            content = response.content[0].text if isinstance(response.content, list) else response.content
        else:
            content = str(response)
            
        result = json.loads(content)
        intent: IntentType = result.get("intent", "SEARCH")
    except (json.JSONDecodeError, AttributeError, IndexError):
        intent = "SEARCH"
    
    node_map = {
        "SEARCH": "search",
        "VERIFY": "verify",
        "CODE_REVIEW": "code_review",
        "AUTONOMOUS": "autonomous"
    }
    
    state["next_node"] = node_map.get(intent, "search")
    return state


def search_rules_node(state: AgentState) -> AgentState:
    """Search rules using RAG or search for files"""
    from src.agent.tools import FileSearchTool
    llm = get_llm_client()
    
    message = state.get("message", "")
    
    # Check if asking for file search
    if any(keyword in message.lower() for keyword in ["파일", "file", "찾", "search", "controller", "service"]):
        # Try file search first
        file_tool = FileSearchTool()
        
        # Extract search term
        search_term = message.lower()
        for word in ["찾아", "찾아줘", "파일", "file", "search"]:
            search_term = search_term.replace(word, "").strip()
        
        results = file_tool.search_files(search_term)
        
        if results:
            file_list = "\n".join([f"- {r['name']} ({r['path']})" for r in results])
            state["final_response"] = f"다음 파일을 찾았습니다:\n\n{file_list}\n\n더 자세히 보려면 파일명을 말씀해주세요."
            state["next_node"] = "complete"
            return state
    
    # Fall back to LLM-based search
    # Use RAG-based Rule Search
    from src.agent.tools import RuleSearchTool
    rule_tool = RuleSearchTool()
    rag_result = rule_tool.search(message)
    
    if "❌" in rag_result:
        # Fallback to general LLM if no rules found
        prompt = f"""사용자 질문에 대해 도움이 되는 답변을 제공하세요.
        
        질문: {message}
        
        특별한 프로젝트 규칙이 발견되지 않았으니, 일반적인 개발 지식을 바탕으로 답변해주세요."""
        
        response = llm.chat([
            {"role": "system", "content": "You are a helpful developer assistant."},
            {"role": "user", "content": prompt}
        ])
        
        # Robust content extraction
        try:
            if hasattr(response, 'choices'):  # OpenAI
                content = response.choices[0].message.content
            elif hasattr(response, 'content'):  # Anthropic
                content = response.content[0].text if isinstance(response.content, list) else response.content
            else:
                content = str(response)
        except (AttributeError, IndexError):
            content = str(response)
    else:
        # Generate response using RAG result
        prompt = f"""사용자 질문에 대해 검색된 프로젝트 규칙을 참고하여 답변하세요.
        
        질문: {message}
        
        [검색된 규칙]
        {rag_result}
        
        위 규칙을 바탕으로 친절하게 설명해주세요. 규칙에 없는 내용은 일반적인 지식으로 보완하되, 규칙을 우선시하세요."""
        
        response = llm.chat([
            {"role": "system", "content": "You are a helpful developer assistant. Use the provided rules to answer."},
            {"role": "user", "content": prompt}
        ])
        
        # Robust content extraction
        try:
            if hasattr(response, 'choices'):  # OpenAI
                content = response.choices[0].message.content
            elif hasattr(response, 'content'):  # Anthropic
                content = response.content[0].text if isinstance(response.content, list) else response.content
            else:
                content = str(response)
        except (AttributeError, IndexError):
            content = str(response)

    state["final_response"] = content
    state["next_node"] = "complete"
    return state


def verify_rules_node(state: AgentState) -> AgentState:
    """Verify code against project rules"""
    llm = get_llm_client()
    
    user_code = state.get("user_code") or state.get("message", "")
    
    prompt = f"""제출된 코드가 프로젝트 규칙에 맞는지 검증하세요.

[코드]
{user_code}

[규칙]
- @RequestMapping 대신 @GetMapping/@PostMapping 사용
- 컨트롤러에서 직접 Repository 호출 금지
- 메서드명은 동사로 시작

검증 결과를 JSON으로 반환:
{{"is_valid": true/false, "violations": ["위반사항1", "위반사항2"], "suggestions": ["개선안1"]}}"""

    response = llm.chat([
        {"role": "system", "content": "You are a code validator. Respond only with JSON."},
        {"role": "user", "content": prompt}
    ])
    
    content = response.choices[0].message.content if hasattr(response, 'choices') else str(response)
    
    try:
        state["validation_result"] = json.loads(content)
    except json.JSONDecodeError:
        state["validation_result"] = {"is_valid": False, "violations": ["파싱 오류"], "suggestions": []}
    
    state["final_response"] = content
    state["next_node"] = "complete"
    return state


def code_review_node(state: AgentState) -> AgentState:
    """Code review agent - reviews style, bugs, performance, security"""
    llm = get_llm_client()
    
    user_code = state.get("user_code") or state.get("message", "")
    
    prompt = f"""시니어 개발자로서 아래 코드를 검수하세요.

[코드]
{user_code}

다음 항목을 검토하고 JSON으로 결과를 반환:
1. style: 코딩 스타일 이슈
2. bugs: 잠재적 버그
3. performance: 성능 개선점
4. security: 보안 취약점
5. summary: 종합 평가
6. score: 점수 (1-10)

형식:
{{
  "style": [{{"line": 1, "issue": "...", "severity": "warning"}}],
  "bugs": [],
  "performance": [],
  "security": [],
  "summary": "...",
  "score": 7
}}"""

    response = llm.chat([
        {"role": "system", "content": "You are a senior code reviewer. Respond only with JSON."},
        {"role": "user", "content": prompt}
    ])
    
    content = response.choices[0].message.content if hasattr(response, 'choices') else str(response)
    
    try:
        state["code_review_result"] = json.loads(content)
    except json.JSONDecodeError:
        state["code_review_result"] = {"summary": content, "score": 0}
    
    state["final_response"] = content
    state["next_node"] = "complete"
    return state


def think_node(state: AgentState) -> AgentState:
    """Autonomous agent - Think step"""
    llm = get_llm_client()
    
    prompt = f"""현재 태스크를 분석하고 다음 행동을 생각하세요.

[태스크] {state.get("task_description") or state.get("message", "")}
[완료된 단계] {state.get("steps_completed", 0)}
[이전 관찰] {state.get("last_observation", "없음")}

다음에 무엇을 해야 하는지 생각하세요."""

    response = llm.chat([
        {"role": "system", "content": "You are an autonomous agent. Think step by step."},
        {"role": "user", "content": prompt}
    ])
    
    if hasattr(response, 'choices'):
        content = response.choices[0].message.content
    elif hasattr(response, 'content'):
        content = response.content[0].text if isinstance(response.content, list) else response.content
    else:
        content = str(response)
    state["current_thought"] = content
    return state


def act_node(state: AgentState) -> AgentState:
    """Autonomous agent - Act step"""
    llm = get_llm_client()
    
    prompt = f"""생각을 바탕으로 행동을 실행하세요.

[생각] {state.get("current_thought", "")}

실행 결과를 반환하세요."""

    response = llm.chat([
        {"role": "system", "content": "You are an autonomous agent executing actions."},
        {"role": "user", "content": prompt}
    ])
    
    content = response.choices[0].message.content if hasattr(response, 'choices') else str(response)
    state["action_result"] = content
    state["last_observation"] = content
    state["steps_completed"] = state.get("steps_completed", 0) + 1
    return state


def should_continue(state: AgentState) -> str:
    """Determine if autonomous loop should continue"""
    max_steps = state.get("max_steps", 5)
    steps = state.get("steps_completed", 0)
    
    if steps >= max_steps:
        return "complete"
    if state.get("error"):
        return "complete"
    if "TASK_COMPLETE" in state.get("last_observation", ""):
        return "complete"
    
    return "continue"


def complete_node(state: AgentState) -> AgentState:
    """Finalize response"""
    if not state.get("final_response"):
        state["final_response"] = state.get("last_observation") or state.get("current_thought", "완료되었습니다.")
    return state
