"""
Test Script - Query Pinecone to verify documents were uploaded.

Usage:
    python test_pinecone.py

This script:
1. Connects to Pinecone
2. Tests with a sample query
3. Shows retrieved documents
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_pinecone_connection():
    """Test connection to Pinecone and query."""
    try:
        from app.core.config import Settings
        from app.services.embeddings_service import EmbeddingsService
        from app.services.pinecone_service import PineconeService
        
        logger.info("\n" + "="*70)
        logger.info("🧪 TESTING PINECONE CONNECTION")
        logger.info("="*70 + "\n")
        
        # Load settings
        settings = Settings()
        logger.info(f"✅ Settings loaded")
        logger.info(f"   📌 Pinecone Index: {settings.pinecone_index}")
        logger.info(f"   🌍 Environment: {settings.pinecone_environment}")
        
        # Initialize services
        logger.info(f"\n🧠 Initializing embeddings service...")
        embeddings_service = EmbeddingsService(
            model_name=settings.embeddings_model
        )
        logger.info(f"✅ Embeddings service ready")
        logger.info(f"   Model: {settings.embeddings_model}")
        
        logger.info(f"\n📌 Initializing Pinecone service...")
        pinecone_service = PineconeService(
            api_key=settings.pinecone_api_key,
            index_name=settings.pinecone_index,
            environment=settings.pinecone_environment
        )
        logger.info(f"✅ Pinecone service ready")
        
        # Test query
        test_query = "What are government policies?"
        logger.info(f"\n🔍 Testing with query: '{test_query}'")
        
        # Generate embedding for query
        query_embedding = embeddings_service.embed_query(test_query)
        logger.info(f"✅ Generated query embedding (dimension: {len(query_embedding)})")
        
        # Query Pinecone
        logger.info(f"\n📤 Querying Pinecone...")
        results = pinecone_service.query_vectors(
            query_embedding=query_embedding,
            country_filter="GLOBAL",
            top_k=3
        )
        
        if results:
            logger.info(f"✅ Found {len(results)} results!\n")
            
            for i, result in enumerate(results, 1):
                logger.info(f"{'─'*70}")
                logger.info(f"Result #{i}")
                logger.info(f"{'─'*70}")
                logger.info(f"📄 Source: {result.get('source', 'Unknown')}")
                logger.info(f"📍 Chunk: {result.get('chunk_index', 'N/A')}")
                logger.info(f"📊 Score: {result.get('score', 'N/A')}")
                text_preview = result.get('text', '')[:200]
                logger.info(f"📝 Text Preview:\n   {text_preview}...")
                logger.info()
        else:
            logger.warning(f"⚠️ No results found!")
            logger.info(f"   This means either:")
            logger.info(f"   1. No documents have been uploaded yet")
            logger.info(f"   2. Documents don't match the query")
            logger.info(f"\n   📚 To upload documents, run: python ingest_pdfs_simple.py")
        
        logger.info(f"{'='*70}")
        logger.info(f"🎉 TEST COMPLETE!")
        logger.info(f"{'='*70}\n")
        
        return len(results) > 0
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    try:
        success = test_pinecone_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
