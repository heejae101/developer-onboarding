"""
API Schemas (Request/Response DTOs)
"""
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, TypeVar, Generic, Any

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope"""
    model_config = ConfigDict(
        exclude_none=True,
        json_encoders={
            datetime: lambda value: value.isoformat(),
            Decimal: lambda value: str(value),
            UUID: lambda value: str(value),
        }
    )
    code: int = Field(200, description="HTTP-like status code")
    message: str = Field("성공했습니다.", description="Result message")
    data: Optional[T] = Field(None, description="Response payload")
    error: Optional[dict[str, Any]] = Field(None, description="Error payload with code/message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response time")
    meta: Optional[dict[str, Any]] = Field(None, description="Additional metadata")


class ChatRequest(BaseModel):
    """Chat request from client"""
    message: str = Field(..., description="User message")
    thread_id: Optional[str] = Field(None, description="Thread ID for conversation context")
    user_code: Optional[str] = Field(None, description="Code to review/verify")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "API 규칙 알려줘",
                "thread_id": "user-123-session-1"
            }
        }


class ChatResponse(BaseModel):
    """Chat response to client"""
    response: str
    intent: Optional[str] = None
    metadata: Optional["ChatMetadata"] = None


class ChatMetadata(BaseModel):
    """Chat response metadata"""
    model_config = ConfigDict(exclude_none=True)
    thread_id: Optional[str] = None
    validation_result: Optional[dict[str, Any]] = None
    code_review_result: Optional[dict[str, Any]] = None


class AgentTaskRequest(BaseModel):
    """Autonomous agent task request"""
    description: str = Field(..., description="Task description")
    max_steps: int = Field(5, ge=1, le=20, description="Maximum steps for autonomous execution")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "rules.md 기반으로 UserController 생성해줘",
                "max_steps": 10
            }
        }


class AgentTaskResponse(BaseModel):
    """Agent task response"""
    task_id: str
    status: Literal["pending", "running", "completed", "failed"]
    result: Optional[str] = None
    steps_completed: int = 0
    error: Optional[str] = None


class CodeReviewRequest(BaseModel):
    """Code review request"""
    code: str = Field(..., description="Code to review")
    language: str = Field("java", description="Programming language")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "@RestController\npublic class UserController {}",
                "language": "java"
            }
        }


class CodeReviewResponse(BaseModel):
    """Code review response"""
    style: list[dict] = []
    bugs: list[dict] = []
    performance: list[dict] = []
    security: list[dict] = []
    summary: str
    score: int = Field(..., ge=0, le=10)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    llm_mode: str
    llm_provider: str
