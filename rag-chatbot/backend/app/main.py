"""
FastAPI application entry point.
Initializes the application, services, and middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .core.config import settings
from .services.pinecone_service import PineconeService
from .services.llm_service import LLMService
from .services.embeddings_service import EmbeddingsService
from .services.rag_pipeline import RAGPipeline
from .routes import chat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global service instances
pinecone_service: PineconeService = None
llm_service: LLMService = None
rag_pipeline: RAGPipeline = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI application.
    Handles startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("🚀 Starting RAG Chatbot application...")
    
    try:
        # Initialize services
        global pinecone_service, llm_service, rag_pipeline
        
        pinecone_service = PineconeService(
            api_key=settings.pinecone_api_key,
            index_name=settings.pinecone_index,
            environment=settings.pinecone_environment
        )
        logger.info("✅ Pinecone service initialized")
        
        llm_service = LLMService(
            api_key=settings.grok_api_key,
            model=settings.llm_model
        )
        logger.info("✅ Grok LLM service initialized")
        
        rag_pipeline = RAGPipeline(
            grok_api_key=settings.grok_api_key,
            embeddings_model=settings.embeddings_model,
            pinecone_service=pinecone_service,
            llm_service=llm_service
        )
        logger.info("✅ RAG Pipeline initialized (ALL FREE: HuggingFace + Grok + Pinecone)")
        
        # Set the pipeline in the chat router
        chat.rag_pipeline = rag_pipeline
        
        logger.info("✅ All services initialized successfully")
        yield
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {str(e)}")
        raise
    
    # Shutdown
    logger.info("🛑 Shutting down RAG Chatbot application...")
    logger.info("✅ Application shut down successfully")


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Production-ready RAG-based chatbot for government policy Q&A",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to RAG Chatbot API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
