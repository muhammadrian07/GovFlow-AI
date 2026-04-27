"""
Pinecone vector database service.
Handles embedding storage and retrieval operations.
"""

from pinecone import Pinecone
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PineconeService:
    """
    Service for interacting with Pinecone vector database.
    Manages vector storage, retrieval, and metadata filtering.
    """
    
    def __init__(self, api_key: str, index_name: str, environment: str = "us-east-1"):
        """
        Initialize Pinecone service.
        
        Args:
            api_key: Pinecone API key
            index_name: Name of the Pinecone index
            environment: Pinecone environment region
        """
        self.api_key = api_key
        self.index_name = index_name
        self.environment = environment
        
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)
        logger.info(f"Pinecone service initialized with index: {index_name}")
    
    def query_vectors(
        self,
        query_embedding: List[float],
        country_filter: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query similar vectors from Pinecone with metadata filtering.
        
        Args:
            query_embedding: Vector embedding of the query
            country_filter: Country to filter by
            top_k: Number of top results to return
            
        Returns:
            List of matching documents with metadata
        """
        try:
            # Query with metadata filter
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                filter={
                    "country": {"$eq": country_filter}
                },
                include_metadata=True
            )
            
            # Extract documents from results
            documents = []
            for match in results.get("matches", []):
                doc = {
                    "id": match.get("id"),
                    "score": match.get("score"),
                    "text": match.get("metadata", {}).get("text", ""),
                    "source": match.get("metadata", {}).get("source", "Unknown"),
                    "page": match.get("metadata", {}).get("page"),
                    "country": match.get("metadata", {}).get("country")
                }
                documents.append(doc)
            
            logger.info(f"Retrieved {len(documents)} documents from Pinecone for country: {country_filter}")
            return documents
        
        except Exception as e:
            logger.error(f"Error querying Pinecone: {str(e)}")
            raise
    
    def upsert_vectors(self, vectors: List[tuple]) -> None:
        """
        Upload vectors to Pinecone.
        
        Args:
            vectors: List of tuples (id, embedding, metadata)
        """
        try:
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            logger.info(f"Upserted {len(vectors)} vectors to Pinecone")
        except Exception as e:
            logger.error(f"Error upserting vectors to Pinecone: {str(e)}")
            raise
    
    def upsert_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> None:
        """
        Upload documents with embeddings to Pinecone.
        
        Args:
            documents: List of document dictionaries with metadata
            embeddings: List of corresponding embeddings
            
        Raises:
            ValueError: If documents and embeddings lengths don't match
        """
        if len(documents) != len(embeddings):
            raise ValueError("Documents and embeddings must have the same length")
        
        try:
            # Prepare vectors for upsert
            vectors_to_upsert = []
            for doc, embedding in zip(documents, embeddings):
                vector = (
                    doc.get("id", f"doc-{len(vectors_to_upsert)}"),
                    embedding,
                    {
                        "text": doc.get("text", ""),
                        "source": doc.get("source", "Unknown"),
                        "page": doc.get("page"),
                        "country": doc.get("country", "USA")
                    }
                )
                vectors_to_upsert.append(vector)
            
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            logger.info(f"Upserted {len(vectors_to_upsert)} documents to Pinecone")
        
        except Exception as e:
            logger.error(f"Error upserting to Pinecone: {str(e)}")
            raise
    
    def delete_vectors(self, ids: List[str]) -> None:
        """
        Delete vectors from Pinecone by ID.
        
        Args:
            ids: List of vector IDs to delete
        """
        try:
            self.index.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} vectors from Pinecone")
        except Exception as e:
            logger.error(f"Error deleting from Pinecone: {str(e)}")
            raise
