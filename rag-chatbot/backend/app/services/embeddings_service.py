"""
Embeddings service using FREE HuggingFace models.
No API keys needed - runs locally or uses HuggingFace inference API (free tier).
"""

from typing import List
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class EmbeddingsService:
    """
    Service for generating embeddings using free HuggingFace models.
    
    Features:
    - No API key required
    - Free models available
    - Works offline or online
    - Good quality for government documents
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embeddings service with HuggingFace model.
        
        Args:
            model_name: HuggingFace model name
                - all-MiniLM-L6-v2: Fast, lightweight, FREE
                - all-mpnet-base-v2: Better quality, slightly slower
                - paraphrase-MiniLM-L6-v2: Good for paraphrasing
                
        Popular FREE models for government content:
        - all-MiniLM-L6-v2 (384 dim) - Fastest, good quality
        - paraphrase-MiniLM-L6-v2 (384 dim) - Good for policy
        - all-mpnet-base-v2 (768 dim) - Best quality
        """
        self.model_name = model_name
        logger.info(f"Loading HuggingFace embeddings model: {model_name}")
        
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"✅ Embeddings model loaded: {model_name}")
        except Exception as e:
            logger.error(f"Error loading embeddings model: {str(e)}")
            raise
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            query: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            embedding = self.model.encode(query, convert_to_tensor=False)
            logger.debug(f"Generated query embedding (dimension: {len(embedding)})")
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        
        Args:
            documents: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(documents, convert_to_tensor=False)
            logger.info(f"Generated embeddings for {len(documents)} documents (dimension: {len(embeddings[0])})")
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating document embeddings: {str(e)}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        test_embedding = self.embed_query("test")
        return len(test_embedding)
