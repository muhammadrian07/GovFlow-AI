"""
RAG (Retrieval-Augmented Generation) Pipeline.
Orchestrates the entire flow: embedding → retrieval → generation.

Uses FREE services:
- HuggingFace embeddings (no API key)
- Groq LLM (free tier)
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
    - Groq for LLM generation (free)
    - Pinecone for vector storage (free tier)
    """
    
    def __init__(
        self,
        groq_api_key: str,
        embeddings_model: str,
        pinecone_service: PineconeService,
        llm_service: LLMService
    ):
        """
        Initialize RAG pipeline with FREE services.
        
        Args:
            groq_api_key: Groq API key for LLM
            embeddings_model: HuggingFace model name for embeddings
            pinecone_service: Initialized Pinecone service
            llm_service: Initialized LLM service (Groq-based)
        """
        self.groq_api_key = groq_api_key
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
        
        Hybrid approach:
        1. First tries RAG (retrieval + generation) if documents exist in Pinecone
        2. Falls back to direct LLM if no relevant documents found (general questions)
        
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
            
            # Step 3: Filter by relevance threshold (0.5 minimum score)
            # Scores range from 0 to 1, where 1 is exact match
            relevance_threshold = 0.5
            relevant_docs = [doc for doc in retrieved_docs if doc.get("score", 0) >= relevance_threshold]
            
            if not relevant_docs or len(relevant_docs) == 0:
                logger.info(f"⚠️ No relevant documents retrieved (threshold: {relevance_threshold}) for query: {query[:50]}...")
                logger.info("📢 Falling back to direct LLM response for general questions...")
                
                # Fallback: Call LLM directly without context for general questions
                answer = self.llm_service.generate_answer_without_context(query)
                logger.info("✅ Answer generated from Groq LLM (general response, no RAG context)")
                
                return {
                    "answer": answer,
                    "sources": [],
                    "model": f"{self.llm_service.model} (General Mode)"
                }
            
            logger.info(f"✅ Retrieved {len(relevant_docs)} relevant documents from Pinecone (score >= {relevance_threshold})")
            logger.info("📚 Using RAG mode (retrieval + generation with context)")
            
            # Step 4: Extract context chunks from documents
            context_chunks = [doc.get("text", "") for doc in relevant_docs]
            
            # Step 5: Generate answer using Groq LLM with context (Groq FREE)
            answer = self.llm_service.generate_answer(query, context_chunks)
            logger.info("✅ Answer generated from Groq LLM with RAG context")
            
            # Step 6: Extract and format sources
            sources = self.llm_service.extract_sources(relevant_docs)
            
            # Step 7: Return complete response
            response = {
                "answer": answer,
                "sources": sources,
                "model": f"{self.llm_service.model} (RAG Mode)"
            }
            
            logger.info("Query processing completed successfully (RAG with FREE SERVICES)")
            return response
        
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            raise
