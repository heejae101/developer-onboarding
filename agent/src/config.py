"""
Configuration module for Agent Service
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # LLM Configuration
    llm_mode: str = "api"  # api | local
    llm_provider: str = "openai"  # openai | anthropic
    embedding_provider: str = "ollama" # openai | ollama
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Ollama Configuration (for local mode)
    ollama_model: str = "llama3"
    ollama_base_url: str = "http://localhost:11434"
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/onboarding"
    redis_url: str = "redis://localhost:6379/0"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Spring Backend
    spring_backend_url: str = "http://localhost:8080"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
