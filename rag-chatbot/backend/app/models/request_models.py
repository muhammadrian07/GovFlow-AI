"""
Pydantic models for request/response validation.
Ensures type safety and automatic API documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Attributes:
        query: User's question or prompt
        country: Country filter for context retrieval (USA, UK, etc.)
        top_k: Number of top results to retrieve (default: 5)
    """
    query: str = Field(..., min_length=1, max_length=500, description="User query")
    country: str = Field(..., description="Country filter (e.g., USA, UK)")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of documents to retrieve")


class SourceReference(BaseModel):
    """
    Metadata for source documents in response.
    
    Attributes:
        text: The relevant chunk of text from the source
        source: File name or document identifier
        page: Page number (if applicable)
    """
    text: str = Field(..., description="Relevant text chunk from source")
    source: str = Field(..., description="Source file name")
    page: Optional[int] = Field(None, description="Page number")


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Attributes:
        answer: Generated answer from RAG pipeline
        sources: List of source documents used for context
        model: Model used for generation
    """
    answer: str = Field(..., description="Generated answer")
    sources: List[SourceReference] = Field(default_factory=list, description="Source documents")
    model: str = Field(default="gpt-3.5-turbo", description="Model used")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
