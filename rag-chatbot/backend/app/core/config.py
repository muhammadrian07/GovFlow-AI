"""
Configuration management for the RAG Chatbot application.
Handles environment variables and global settings.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All services use FREE tiers - perfect for students!
    
    Attributes:
        pinecone_api_key: API key for Pinecone vector database (FREE tier)
        pinecone_index: Index name in Pinecone
        pinecone_environment: Pinecone environment region
        grok_api_key: API key for Grok AI LLM (FREE)
        embeddings_model: Free embeddings model name (HuggingFace)
        debug: Debug mode flag
        cors_origins: List of allowed CORS origins
    """
    
    # Pinecone Configuration (FREE tier available)
    pinecone_api_key: str
    pinecone_index: str = "govflow-index"
    pinecone_environment: str = "us-east-1"
    
    # Grok AI Configuration (FREE with API key)
    grok_api_key: str
    llm_model: str = "grok-1"
    
    # Embeddings Configuration (FREE - HuggingFace models, no API key needed)
    embeddings_model: str = "all-MiniLM-L6-v2"  # Free, fast, high quality
    embeddings_provider: str = "huggingface"
    
    # Application Configuration
    debug: bool = True
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
