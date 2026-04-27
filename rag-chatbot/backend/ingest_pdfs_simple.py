"""
Simple PDF Ingestion Script - Upload documents to Pinecone.

This is a standalone script that can be run directly.

Usage:
    python ingest_pdfs_simple.py

Before running:
1. Place your PDF files in the knowledge_base/ folder
2. Make sure you have created .env file with:
   - PINECONE_API_KEY
   - PINECONE_INDEX
   - PINECONE_ENVIRONMENT
3. Run: pip install -r requirements.txt
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import logging
from dotenv import load_dotenv

# Add current directory to path to find app module
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_config():
    """Get configuration from environment variables."""
    config = {
        "pinecone_api_key": os.getenv("PINECONE_API_KEY"),
        "pinecone_index": os.getenv("PINECONE_INDEX", "starter-index"),
        "pinecone_environment": os.getenv("PINECONE_ENVIRONMENT", "us-east-1"),
        "embeddings_model": os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2"),
    }
    
    if not config["pinecone_api_key"]:
        raise ValueError("❌ PINECONE_API_KEY not found in .env file!")
    
    logger.info("✅ Configuration loaded from .env")
    return config


def initialize_services(config: Dict):
    """Initialize embeddings and Pinecone services."""
    try:
        from app.services.embeddings_service import EmbeddingsService
        from app.services.pinecone_service import PineconeService
        
        logger.info("🧠 Initializing embeddings service...")
        embeddings_service = EmbeddingsService(model_name=config["embeddings_model"])
        
        logger.info("📌 Initializing Pinecone service...")
        pinecone_service = PineconeService(
            api_key=config["pinecone_api_key"],
            index_name=config["pinecone_index"],
            environment=config["pinecone_environment"]
        )
        
        return embeddings_service, pinecone_service
    except ImportError as e:
        logger.error(f"❌ Import error: {str(e)}")
        logger.error("Make sure you're running this from the backend directory!")
        raise


def get_pdf_files(knowledge_base_dir: Path) -> List[Path]:
    """Get all PDF files from knowledge_base directory."""
    if not knowledge_base_dir.exists():
        logger.warning(f"⚠️ Creating knowledge_base directory: {knowledge_base_dir}")
        knowledge_base_dir.mkdir(parents=True, exist_ok=True)
        return []
    
    pdf_files = list(knowledge_base_dir.glob("*.pdf"))
    logger.info(f"📄 Found {len(pdf_files)} PDF files")
    for pdf_file in pdf_files:
        logger.info(f"   - {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
    
    return pdf_files


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
        
        logger.info(f"📖 Loading PDF: {pdf_path.name}")
        reader = PdfReader(str(pdf_path))
        
        text = ""
        for page_num, page in enumerate(reader.pages):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
        
        logger.info(f"✅ Extracted {len(reader.pages)} pages from {pdf_path.name}")
        return text
    except Exception as e:
        logger.error(f"❌ Error loading PDF {pdf_path.name}: {str(e)}")
        raise


def chunk_text(text: str, source: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Dict]:
    """Split text into chunks with metadata."""
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        logger.info(f"✂️ Split into {len(chunks)} chunks (size: {chunk_size}, overlap: {chunk_overlap})")
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"{source}_chunk_{i}",
                "text": chunk,
                "source": source,
                "chunk_index": i,
                "country": "GLOBAL"
            }
            documents.append(doc)
        
        return documents
    except Exception as e:
        logger.error(f"❌ Error chunking text: {str(e)}")
        raise


def upload_documents(documents: List[Dict], embeddings_service, pinecone_service) -> int:
    """Upload documents to Pinecone with embeddings."""
    try:
        if not documents:
            logger.warning("⚠️ No documents to upload")
            return 0
        
        logger.info(f"🚀 Uploading {len(documents)} documents to Pinecone...")
        
        # Extract text for embedding
        texts = [doc["text"] for doc in documents]
        
        # Generate embeddings using HuggingFace (FREE)
        logger.info(f"🧠 Generating embeddings for {len(texts)} chunks...")
        embeddings = embeddings_service.embed_documents(texts)
        logger.info(f"✅ Generated {len(embeddings)} embeddings")
        
        # Prepare vectors for Pinecone
        vectors_to_upsert = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            vector = (
                doc["id"],
                embedding,
                {
                    "text": doc["text"][:500],  # Store first 500 chars as preview
                    "source": doc["source"],
                    "chunk_index": doc["chunk_index"],
                    "country": doc["country"]
                }
            )
            vectors_to_upsert.append(vector)
        
        # Upload to Pinecone in batches
        batch_size = 100
        total_uploaded = 0
        
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            logger.info(f"📤 Uploading batch {i//batch_size + 1}/{(len(vectors_to_upsert) + batch_size - 1)//batch_size}...")
            pinecone_service.upsert_vectors(batch)
            total_uploaded += len(batch)
        
        logger.info(f"✅ Successfully uploaded {total_uploaded} vectors to Pinecone!")
        return total_uploaded
        
    except Exception as e:
        logger.error(f"❌ Error uploading documents: {str(e)}")
        raise


def main():
    """Main entry point."""
    try:
        logger.info("\n" + "="*70)
        logger.info("🚀 PDF INGESTION PIPELINE - Upload to Pinecone")
        logger.info("="*70 + "\n")
        
        # Get configuration
        config = get_config()
        
        # Initialize services
        embeddings_service, pinecone_service = initialize_services(config)
        
        # Get PDF files
        knowledge_base_dir = Path(__file__).parent / "knowledge_base"
        pdf_files = get_pdf_files(knowledge_base_dir)
        
        if not pdf_files:
            logger.warning("⚠️ No PDF files found!")
            logger.info(f"📁 Please add PDF files to: {knowledge_base_dir.absolute()}")
            return
        
        # Process each PDF
        total_documents = 0
        for pdf_file in pdf_files:
            try:
                logger.info(f"\n{'─'*70}")
                logger.info(f"Processing: {pdf_file.name}")
                logger.info(f"{'─'*70}")
                
                # Extract text
                text = extract_text_from_pdf(pdf_file)
                
                # Chunk text
                documents = chunk_text(text, source=pdf_file.stem)
                
                # Upload to Pinecone
                uploaded = upload_documents(documents, embeddings_service, pinecone_service)
                total_documents += uploaded
                
                logger.info(f"✅ Completed: {pdf_file.name}")
            
            except Exception as e:
                logger.error(f"❌ Failed to process {pdf_file.name}: {str(e)}")
                continue
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🎉 INGESTION COMPLETE!")
        logger.info(f"{'='*70}")
        logger.info(f"📊 Total vectors uploaded: {total_documents}")
        logger.info(f"✅ Documents are now searchable in Pinecone!")
        logger.info(f"{'='*70}\n")
    
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
