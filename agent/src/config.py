"""
Configuration module for Agent Service
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    # LLM Configuration
    llm_mode: str = Field("api", env="LLM_MODE")  # api | local
    llm_provider: str = Field("openai", env="LLM_PROVIDER")  # openai | anthropic | ollama
    embedding_provider: str = Field("ollama", env="EMBEDDING_PROVIDER")  # openai | ollama
    openai_api_key: str = Field("", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field("", env="ANTHROPIC_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    anthropic_model: str = Field("claude-3-haiku-20240307", env="ANTHROPIC_MODEL")
    
    # Ollama Configuration (for local mode)
    ollama_llm_model: str = Field("gpt-oss:20b", env="OLLAMA_LLM_MODEL")
    ollama_embed_model: str = Field("nomic-embed-text", env="OLLAMA_EMBED_MODEL")
    ollama_base_url: str = Field("http://localhost:11434", env="OLLAMA_BASE_URL")
    
    # Database
    database_url: str = Field("postgresql://postgres:password@localhost:5432/onboarding", env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # Server
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    debug: bool = Field(True, env="DEBUG")
    
    # Spring Backend
    spring_backend_url: str = Field("http://localhost:8080", env="SPRING_BACKEND_URL")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
