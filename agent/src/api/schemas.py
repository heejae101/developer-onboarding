"""
API Schemas (Request/Response DTOs)
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal


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
    metadata: Optional[dict] = None


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
