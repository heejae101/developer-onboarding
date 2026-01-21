"""
API Routes
"""
from fastapi import APIRouter, HTTPException
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    AgentTaskRequest,
    AgentTaskResponse,
    CodeReviewRequest,
    CodeReviewResponse,
    HealthResponse,
)
from src.agent import get_agent_graph, AgentState
from src.config import get_settings
from src.api import websocket
import uuid

router = APIRouter()
router.include_router(websocket.router)


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        llm_mode=settings.llm_mode,
        llm_provider=settings.llm_provider
    )


@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat with the AI agent.
    The agent will automatically route to the appropriate handler based on intent.
    """
    try:
        graph = get_agent_graph()
        
        initial_state: AgentState = {
            "thread_id": request.thread_id or str(uuid.uuid4()),
            "user_id": 0,
            "message": request.message,
            "user_code": request.user_code,
        }
        
        result = await graph.ainvoke(initial_state)
        
        return ChatResponse(
            response=result.get("final_response", "응답을 생성할 수 없습니다."),
            intent=result.get("next_node"),
            metadata={
                "thread_id": initial_state["thread_id"],
                "validation_result": result.get("validation_result"),
                "code_review_result": result.get("code_review_result"),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/code-review", response_model=CodeReviewResponse, tags=["Code Review"])
async def review_code(request: CodeReviewRequest):
    """
    Review code for style, bugs, performance, and security issues.
    """
    try:
        graph = get_agent_graph()
        
        initial_state: AgentState = {
            "thread_id": str(uuid.uuid4()),
            "user_id": 0,
            "message": f"다음 {request.language} 코드를 리뷰해줘",
            "user_code": request.code,
            "next_node": "code_review",  # Force code review path
        }
        
        # Directly invoke code review node
        from src.agent.nodes import code_review_node
        result = code_review_node(initial_state)
        
        review_result = result.get("code_review_result", {})
        return CodeReviewResponse(
            style=review_result.get("style", []),
            bugs=review_result.get("bugs", []),
            performance=review_result.get("performance", []),
            security=review_result.get("security", []),
            summary=review_result.get("summary", "리뷰 결과 없음"),
            score=review_result.get("score", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/task", response_model=AgentTaskResponse, tags=["Agent"])
async def create_agent_task(request: AgentTaskRequest):
    """
    Create an autonomous agent task.
    The agent will think, act, and observe in a loop until completion.
    """
    try:
        graph = get_agent_graph()
        task_id = str(uuid.uuid4())
        
        initial_state: AgentState = {
            "thread_id": task_id,
            "user_id": 0,
            "message": request.description,
            "task_description": request.description,
            "max_steps": request.max_steps,
            "steps_completed": 0,
            "completed_steps": [],
            "next_node": "autonomous",
        }
        
        # Force autonomous path by setting next_node
        from src.agent.nodes import think_node, act_node, should_continue, complete_node
        
        state = initial_state
        while should_continue(state) == "continue":
            state = think_node(state)
            state = act_node(state)
        
        state = complete_node(state)
        
        return AgentTaskResponse(
            task_id=task_id,
            status="completed",
            result=state.get("final_response"),
            steps_completed=state.get("steps_completed", 0),
            error=state.get("error")
        )
    except Exception as e:
        return AgentTaskResponse(
            task_id=str(uuid.uuid4()),
            status="failed",
            error=str(e),
            steps_completed=0
        )
