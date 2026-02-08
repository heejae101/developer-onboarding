"""
Admin API Routes - 관리자 설정 API
"""
from typing import Any
from fastapi import APIRouter
from src.api.schemas import ApiResponse
from src.error_codes import INTERNAL_ERROR
from src.graph_settings import (
    GraphSettings,
    get_graph_settings,
    save_graph_settings,
    reset_graph_settings,
    invalidate_graph_cache,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/graph-settings", response_model=ApiResponse[GraphSettings])
async def get_settings():
    """현재 그래프 설정 조회"""
    print("[Admin API] GET /admin/graph-settings - Fetching current settings")
    settings = get_graph_settings()
    print(
        "[Admin API] Returning settings: "
        f"self_rag={settings.enable_self_rag}, "
        f"parallel={settings.enable_parallel_search}, grading={settings.enable_answer_grading}"
    )
    return ApiResponse(data=settings)


@router.put("/graph-settings", response_model=ApiResponse[GraphSettings])
async def update_settings(settings: GraphSettings):
    """그래프 설정 업데이트 (즉시 반영)"""
    print("[Admin API] PUT /admin/graph-settings - Updating settings")
    print(f"   New values: self_rag={settings.enable_self_rag}, "
          f"parallel={settings.enable_parallel_search}, grading={settings.enable_answer_grading}")
    
    try:
        save_graph_settings(settings)
        invalidate_graph_cache()
        print("[Admin API] Settings updated and graph invalidated")
        return ApiResponse(data=settings)
    except Exception as e:
        print(f"[Admin API] Failed to update settings: {e}")
        return ApiResponse(
            code=INTERNAL_ERROR.http_status,
            message="실패했습니다.",
            error={"code": INTERNAL_ERROR.code, "message": INTERNAL_ERROR.message},
        )


@router.patch("/graph-settings", response_model=ApiResponse[GraphSettings])
async def patch_settings(updates: dict):
    """그래프 설정 일부만 업데이트"""
    print(f"[Admin API] PATCH /admin/graph-settings - Partial update: {updates}")
    
    try:
        current = get_graph_settings()
        updated = current.model_copy(update=updates)
        save_graph_settings(updated)
        invalidate_graph_cache()
        print("[Admin API] Partial settings updated and graph invalidated")
        return ApiResponse(data=updated)
    except Exception as e:
        print(f"[Admin API] Failed to patch settings: {e}")
        return ApiResponse(
            code=INTERNAL_ERROR.http_status,
            message="실패했습니다.",
            error={"code": INTERNAL_ERROR.code, "message": INTERNAL_ERROR.message},
        )


@router.post("/graph-settings/reset", response_model=ApiResponse[GraphSettings])
async def reset_settings():
    """설정을 기본값으로 초기화"""
    print("[Admin API] POST /admin/graph-settings/reset - Resetting to defaults")
    
    settings = reset_graph_settings()
    invalidate_graph_cache()
    
    print("[Admin API] Settings reset to defaults and graph invalidated")
    return ApiResponse(data=settings)


@router.get("/graph-visualization", response_model=ApiResponse[dict[str, Any]])
async def get_graph_visualization():
    """현재 그래프 구조 시각화 정보 반환 (Mermaid 형식)"""
    print("[Admin API] GET /admin/graph-visualization - Generating graph diagram")
    
    settings = get_graph_settings()
    
    # Mermaid 다이어그램 생성
    mermaid = ["flowchart TB"]
    mermaid.append("    R[router]")
    
    if settings.enable_self_rag:
        mermaid.append("    subgraph SelfRAG[Self-RAG Loop]")
        mermaid.append("        S[search] --> E[evaluate]")
        mermaid.append("        E -->|부족| S")
        mermaid.append("        E -->|충분| SY[synthesize]")
        mermaid.append("    end")
        mermaid.append("    R --> S")
    else:
        mermaid.append("    S[search]")
        mermaid.append("    R --> S")
        mermaid.append("    S --> C")
    
    if settings.enable_answer_grading:
        mermaid.append("    subgraph AnswerGrading[Answer Quality Loop]")
        mermaid.append("        G[grade] -->|낮음| RF[refine]")
        mermaid.append("        RF --> G")
        mermaid.append("        G -->|OK| C[complete]")
        mermaid.append("    end")
        if settings.enable_self_rag:
            mermaid.append("    SY --> G")
    else:
        mermaid.append("    C[complete]")
        if settings.enable_self_rag:
            mermaid.append("    SY --> C")
    
    mermaid.append("    V[verify] --> C")
    mermaid.append("    CR[code_review] --> C")
    mermaid.append("    R --> V")
    mermaid.append("    R --> CR")
    mermaid.append("    C --> END[END]")
    
    result = {
        "settings": settings.model_dump(),
        "mermaid": "\n".join(mermaid),
        "active_patterns": {
            "self_rag": settings.enable_self_rag,
            "parallel_search": settings.enable_parallel_search,
            "answer_grading": settings.enable_answer_grading,
            "human_approval": settings.enable_human_approval,
        }
    }
    
    print(f"[Admin API] Visualization generated with {len(mermaid)} nodes")
    return ApiResponse(data=result)
