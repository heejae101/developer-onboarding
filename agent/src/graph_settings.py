"""
Graph Settings Module - 관리자가 설정 가능한 그래프 패턴 설정
"""
from pydantic import BaseModel, Field
from typing import Optional
import json
from pathlib import Path


class GraphSettings(BaseModel):
    """그래프 패턴 설정 - 관리자 페이지에서 ON/OFF 가능"""
    
    # ===== Self-RAG 패턴 =====
    # RAG 검색 결과를 평가하고, 부족하면 재검색
    enable_self_rag: bool = Field(
        default=True,
        description="Self-RAG 활성화: 검색 결과 평가 → 부족하면 재검색"
    )
    max_search_retries: int = Field(
        default=2,
        ge=1,
        le=5,
        description="최대 재검색 횟수"
    )
    relevance_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="관련성 임계값 (이하면 재검색)"
    )
    
    # ===== 병렬 검색 패턴 =====
    # RAG + 파일검색을 동시에 실행
    enable_parallel_search: bool = Field(
        default=True,
        description="병렬 검색 활성화: RAG + 파일검색 동시 실행"
    )
    parallel_sources: list[str] = Field(
        default=["rag", "file"],
        description="병렬 검색 소스 목록"
    )
    
    # ===== Answer Grading 패턴 =====
    # 답변 품질을 평가하고, 낮으면 개선
    enable_answer_grading: bool = Field(
        default=True,
        description="답변 품질 평가 활성화: 품질 낮으면 개선 루프"
    )
    min_answer_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="최소 답변 품질 점수 (이하면 개선)"
    )
    max_refine_attempts: int = Field(
        default=2,
        ge=1,
        le=5,
        description="최대 답변 개선 횟수"
    )
    
    # ===== Human-in-the-loop 패턴 =====
    # 중요 결정에서 사용자 확인 요청
    enable_human_approval: bool = Field(
        default=False,
        description="사용자 확인 요청 활성화: 중요 결정 시 승인 요청"
    )
    approval_actions: list[str] = Field(
        default=["file_create", "code_execute"],
        description="승인이 필요한 액션 목록"
    )
    
    # ===== 디버그/로깅 =====
    enable_step_logging: bool = Field(
        default=True,
        description="각 노드 실행 로그 출력"
    )


# 설정 파일 경로
SETTINGS_FILE = Path(__file__).parent / "graph_settings.json"

# 런타임 설정 (싱글톤)
_runtime_settings: Optional[GraphSettings] = None


def get_graph_settings() -> GraphSettings:
    """현재 그래프 설정 반환 (캐시됨)"""
    global _runtime_settings
    
    if _runtime_settings is None:
        _runtime_settings = load_graph_settings()
    
    return _runtime_settings


def load_graph_settings() -> GraphSettings:
    """파일에서 설정 로드 (없으면 기본값)"""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return GraphSettings(**data)
        except (json.JSONDecodeError, ValueError):
            pass
    
    return GraphSettings()


def save_graph_settings(settings: GraphSettings) -> None:
    """설정을 파일에 저장"""
    global _runtime_settings
    
    print("[Settings] Saving new configuration...")
    print(f"   - Self-RAG: {settings.enable_self_rag}")
    print(f"   - Parallel Search: {settings.enable_parallel_search}")
    print(f"   - Answer Grading: {settings.enable_answer_grading}")
    
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings.model_dump(), f, indent=2, ensure_ascii=False)
    
    # 런타임 설정 즉시 업데이트
    _runtime_settings = settings
    print("[Settings] Configuration saved and runtime updated")


def update_graph_settings(**kwargs) -> GraphSettings:
    """설정 일부만 업데이트"""
    current = get_graph_settings()
    updated = current.model_copy(update=kwargs)
    save_graph_settings(updated)
    return updated


def reset_graph_settings() -> GraphSettings:
    """설정을 기본값으로 초기화"""
    global _runtime_settings
    
    if SETTINGS_FILE.exists():
        SETTINGS_FILE.unlink()
    
    _runtime_settings = GraphSettings()
    return _runtime_settings


def invalidate_graph_cache() -> None:
    """그래프 캐시 무효화 (설정 변경 후 그래프 재빌드 필요)"""
    global _runtime_settings
    _runtime_settings = None
    
    # graph.py의 싱글톤도 무효화
    from src.agent.graph import invalidate_graph
    invalidate_graph()
