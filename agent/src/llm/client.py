"""
LLM Client module - Supports both API (OpenAI/Anthropic) and Local (Ollama) modes
"""
from abc import ABC, abstractmethod
from typing import Generator, Any
from src.config import get_settings


class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def chat(self, messages: list[dict], stream: bool = False) -> Any:
        """Send chat request to LLM"""
        pass
    
    @abstractmethod
    def chat_stream(self, messages: list[dict]) -> Generator[str, None, None]:
        """Stream chat response from LLM"""
        pass
    
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate embedding for text"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client"""
    
    def __init__(self, model: str | None = None):
        from openai import OpenAI
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = model or settings.openai_model
    
    def chat(self, messages: list[dict], stream: bool = False) -> Any:
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream
        )
    
    def chat_stream(self, messages: list[dict]) -> Generator[str, None, None]:
        response = self.chat(messages, stream=True)
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    
    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding


class AnthropicClient(LLMClient):
    """Anthropic API client"""
    
    def __init__(self, model: str | None = None):
        from anthropic import Anthropic
        settings = get_settings()
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = model or settings.anthropic_model
    
    def chat(self, messages: list[dict], stream: bool = False) -> Any:
        # Convert OpenAI format to Anthropic format
        system_msg = ""
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                chat_messages.append(msg)
        
        return self.client.messages.create(
            model=self.model,
            system=system_msg,
            messages=chat_messages,
            max_tokens=4096,
            stream=stream
        )
    
    def chat_stream(self, messages: list[dict]) -> Generator[str, None, None]:
        with self.chat(messages, stream=True) as response:
            for text in response.text_stream:
                yield text
    
    def embed(self, text: str) -> list[float]:
        # Anthropic doesn't have embeddings, fallback to OpenAI
        from openai import OpenAI
        settings = get_settings()
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding


class OllamaClient(LLMClient):
    """Ollama local client"""
    
    def __init__(self, model: str | None = None):
        import ollama
        settings = get_settings()
        self.ollama = ollama
        self.model = model or settings.ollama_llm_model
    
    def chat(self, messages: list[dict], stream: bool = False) -> Any:
        return self.ollama.chat(
            model=self.model,
            messages=messages,
            stream=stream
        )
    
    def chat_stream(self, messages: list[dict]) -> Generator[str, None, None]:
        for chunk in self.ollama.chat(
            model=self.model,
            messages=messages,
            stream=True
        ):
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
    
    def embed(self, text: str) -> list[float]:
        response = self.ollama.embeddings(
            model="nomic-embed-text",
            prompt=text
        )
        return response["embedding"]


def get_llm_client() -> LLMClient:
    """Factory function to get appropriate LLM client based on settings"""
    settings = get_settings()
    
    if settings.llm_mode == "local":
        return OllamaClient()
    elif settings.llm_provider == "anthropic":
        return AnthropicClient()
    else:
        return OpenAIClient()


def get_embedding_client() -> LLMClient:
    """Factory function to get appropriate Embedding client based on settings"""
    settings = get_settings()
    
    if settings.embedding_provider == "ollama":
        return OllamaClient(model=settings.ollama_embed_model)
    else:
        return OpenAIClient()
