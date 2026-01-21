"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api import router
from src.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    settings = get_settings()
    print(f"🚀 Starting Agent Service...")
    print(f"   LLM Mode: {settings.llm_mode}")
    print(f"   LLM Provider: {settings.llm_provider}")
    print(f"   Debug: {settings.debug}")
    
    # Initialize RAG Manager on startup
    try:
        # Check if RAG is possible
        can_run_rag = True
        if settings.embedding_provider == "openai" and not settings.openai_api_key:
            can_run_rag = False
            print("⚠️  RAG Skipped: OpenAI API Key missing for OpenAI Embeddings")
            
        if can_run_rag:
             from src.agent.rag_modules import RAGManager
             RAGManager() # This triggers initialization and logs
    except Exception as e:
        print(f"⚠️  RAG Initialization Failed: {e}")
        
    yield
    # Shutdown
    print("👋 Shutting down Agent Service...")


def create_app() -> FastAPI:
    """Create FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="Onboarding Agent Service",
        description="AI Agent powered by LangGraph for intelligent developer onboarding",
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.debug,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(router, prefix="/api/v1")
    
    # WebSocket router (No prefix or root level)
    from src.api.websocket import router as ws_router
    app.include_router(ws_router)
    
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "service": "Onboarding Agent Service",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app


# Application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
