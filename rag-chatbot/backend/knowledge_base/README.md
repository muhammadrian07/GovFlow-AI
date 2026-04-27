# 📚 Knowledge Base

This folder contains PDF documents that will be ingested and uploaded to Pinecone as vector embeddings.

## 📝 How to Use

### 1. Add Your PDF Files

Place your PDF documents in this folder (`knowledge_base/`):

```
knowledge_base/
├── policy_document_1.pdf
├── government_rules.pdf
├── regulations.pdf
└── ...
```

### 2. Run the Ingestion Script

From the `backend` directory:

```bash
# Make sure you have installed dependencies
pip install -r requirements.txt

# Run the ingestion script
python ingest_pdfs_simple.py
```

### 3. What Happens

The script will:
1. 📖 **Read** all PDF files from this folder
2. ✂️ **Split** documents into chunks (1000 chars each)
3. 🧠 **Generate embeddings** using HuggingFace (FREE, no API key needed!)
4. 📤 **Upload** vectors to Pinecone
5. 🎉 **Make searchable** through your chatbot

## 📊 Processing Details

| Step | Tool | Cost |
|------|------|------|
| PDF Reading | pypdf | FREE |
| Text Chunking | LangChain | FREE |
| Embeddings | HuggingFace | FREE |
| Vector Storage | Pinecone | FREE (100K vectors) |

## ⚙️ Configuration

The script reads from your `.env` file:

```env
# Required for Pinecone upload
PINECONE_API_KEY=your_key_here
PINECONE_INDEX=starter-index
PINECONE_ENVIRONMENT=us-east-1

# Embeddings model (optional, has default)
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

## 📈 Chunk Size Guide

- **Small chunks (500-800 chars)**: Better for Q&A, more vectors
- **Medium chunks (1000 chars)**: Balanced (default)
- **Large chunks (2000+ chars)**: Fewer vectors, less granular

Edit `ingest_pdfs_simple.py` to change chunk size:
```python
documents = chunk_text(text, source=pdf_file.stem, chunk_size=1500)
```

## 📊 Example Output

```
🚀 PDF INGESTION PIPELINE - Upload to Pinecone
======================================================================

📄 Found 2 PDF files
   - policy_document.pdf (256.3 KB)
   - regulations.pdf (180.1 KB)

──────────────────────────────────────────────────────────────────────
Processing: policy_document.pdf
──────────────────────────────────────────────────────────────────────

📖 Loading PDF: policy_document.pdf
✅ Extracted 15 pages from policy_document.pdf
✂️ Split into 42 chunks (size: 1000, overlap: 100)
🧠 Generating embeddings for 42 chunks...
✅ Generated 42 embeddings
🚀 Uploading 42 documents to Pinecone...
📤 Uploading batch 1/1...
✅ Successfully uploaded 42 vectors to Pinecone!

🎉 INGESTION COMPLETE!
======================================================================
📊 Total vectors uploaded: 84
✅ Documents are now searchable in Pinecone!
```

## ❓ FAQ

**Q: What PDF formats are supported?**
A: Standard PDF files (`.pdf`). Images in PDFs will be skipped.

**Q: How many documents can I upload?**
A: Free Pinecone tier: up to 100K vectors. Calculate: `PDF chunks × 1 = vectors`

**Q: Can I add more PDFs later?**
A: Yes! Just add them to the folder and run the script again.

**Q: How do I know it worked?**
A: Test in your chatbot! Query should return answers from your PDFs.

**Q: What if upload fails?**
A: Check your Pinecone API key and index name in `.env`.

## 🚀 Next Steps

1. ✅ Add PDF files here
2. ✅ Run: `python ingest_pdfs_simple.py`
3. ✅ Test in chatbot
4. ✅ Ask questions about your documents!

---

**Happy ingesting! 📚**
