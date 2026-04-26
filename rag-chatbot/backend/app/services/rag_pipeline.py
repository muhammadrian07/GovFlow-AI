"""
RAG (Retrieval-Augmented Generation) Pipeline.
Orchestrates the entire flow: embedding → retrieval → generation.

Uses FREE services:
- HuggingFace embeddings (no API key)
- Grok AI LLM (free tier)
- Pinecone vector DB (free tier)
"""

from .embeddings_service import EmbeddingsService
from .pinecone_service import PineconeService
from .llm_service import LLMService
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Complete RAG pipeline for question answering using FREE services.
    
    Uses:
    - HuggingFace embeddings (free, no API key)
    - Grok AI for LLM generation (free)
    - Pinecone for vector storage (free tier)
    """
    
    def __init__(
        self,
        grok_api_key: str,
        embeddings_model: str,
        pinecone_service: PineconeService,
        llm_service: LLMService
    ):
        """
        Initialize RAG pipeline with FREE services.
        
        Args:
            grok_api_key: Grok API key for LLM
            embeddings_model: HuggingFace model name for embeddings
            pinecone_service: Initialized Pinecone service
            llm_service: Initialized LLM service (Grok-based)
        """
        self.grok_api_key = grok_api_key
        self.pinecone_service = pinecone_service
        self.llm_service = llm_service
        
        # Initialize embeddings with FREE HuggingFace model
        logger.info(f"Initializing embeddings with HuggingFace model: {embeddings_model}")
        self.embeddings_service = EmbeddingsService(model_name=embeddings_model)
        logger.info("✅ RAG Pipeline initialized (ALL FREE: HuggingFace + Grok + Pinecone)")
    
    async def process_query(
        self,
        query: str,
        country: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Process a user query through the complete RAG pipeline using FREE services.
        
        Args:
            query: User's question
            country: Country filter for context
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            logger.info(f"Processing query: {query[:50]}... for country: {country}")
            
            # Step 1: Convert query to embedding (HuggingFace - FREE)
            query_embedding = self.embeddings_service.embed_query(query)
            logger.info("Query embedding generated (HuggingFace - FREE)")
            
            # Step 2: Query Pinecone with metadata filter (Pinecone FREE tier)
            retrieved_docs = self.pinecone_service.query_vectors(
                query_embedding=query_embedding,
                country_filter=country,
                top_k=top_k
            )
            
            if not retrieved_docs:
                logger.warning(f"No documents retrieved for country: {country}")
                return {
                    "answer": "I don't have any documents for the selected country to answer your question.",
                    "sources": [],
                    "model": self.llm_service.model
                }
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents")
            
            # Step 3: Extract context chunks from documents
            context_chunks = [doc.get("text", "") for doc in retrieved_docs]
            
            # Step 4: Generate answer using Grok LLM with context (Grok FREE)
            answer = self.llm_service.generate_answer(query, context_chunks)
            logger.info("Answer generated from Grok LLM (FREE)")
            
            # Step 5: Extract and format sources
            sources = self.llm_service.extract_sources(retrieved_docs)
            
            # Step 6: Return complete response
            response = {
                "answer": answer,
                "sources": sources,
                "model": self.llm_service.model
            }
            
            logger.info("Query processing completed successfully (ALL FREE SERVICES)")
            return response
        
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            raise
