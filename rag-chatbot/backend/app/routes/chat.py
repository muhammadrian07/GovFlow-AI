"""
Chat route handlers.
Defines API endpoints for chatbot interactions.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Any, Dict
import logging

from ..models.request_models import ChatRequest, ChatResponse
from ..services.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["chat"])

# Global RAG pipeline instance (initialized in main.py)
rag_pipeline: RAGPipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """
    Dependency injection for RAG pipeline.
    
    Returns:
        RAGPipeline instance
        
    Raises:
        RuntimeError: If pipeline is not initialized
    """
    if rag_pipeline is None:
        raise RuntimeError("RAG Pipeline not initialized")
    return rag_pipeline


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
) -> ChatResponse:
    """
    Main chat endpoint.
    
    Accepts a user query and country filter, returns RAG-generated answer with sources.
    
    Args:
        request: Chat request with query and country
        pipeline: RAG pipeline dependency
        
    Returns:
        ChatResponse with answer and sources
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        logger.info(f"Received chat request: query='{request.query[:30]}...', country={request.country}")
        
        # Process query through RAG pipeline
        result = await pipeline.process_query(
            query=request.query,
            country=request.country,
            top_k=request.top_k
        )
        
        # Return formatted response
        response = ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            model=result["model"]  # Will be grok-1
        )
        
        logger.info("Chat response sent successfully")
        return response
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your question. Please try again."
        )


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Status information
    """
    return {"status": "healthy", "version": "1.0.0"}
