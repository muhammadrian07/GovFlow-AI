# 📚 PDF Ingestion - Quick Reference

## ✅ What I Created for You

### 1. **knowledge_base Folder** 📁
   - Location: `backend/knowledge_base/`
   - Purpose: Store your PDF files here

### 2. **Ingestion Scripts** 🐍
   - `backend/ingest_pdfs_simple.py` - **USE THIS ONE** ⭐
     - Standalone script (easiest to use)
     - Simple to run and debug
   - `backend/app/scripts/ingest_pdfs.py` - Full-featured version

### 3. **Updated Requirements** 📦
   - Added `pypdf==3.17.1` for PDF reading
   - All dependencies now included

---

## 🚀 Quick Start (3 Steps)

### Step 1: Add Your PDFs
```bash
# Copy your PDF files to:
backend/knowledge_base/
```

### Step 2: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run Ingestion
```bash
python ingest_pdfs_simple.py
```

---

## 📋 What the Script Does

```
Your PDFs in knowledge_base/
        ↓
📖 Read PDF text
        ↓
✂️ Split into 1000-char chunks
        ↓
🧠 Generate embeddings (HuggingFace - FREE)
        ↓
📤 Upload to Pinecone
        ↓
🎉 Your documents are now searchable!
```

---

## 📝 Before Running

Make sure your `.env` file has:

```env
PINECONE_API_KEY=your_key
PINECONE_INDEX=starter-index
PINECONE_ENVIRONMENT=us-east-1
```

---

## 📊 Example Workflow

```bash
# 1. Copy PDFs to knowledge_base folder
cp path/to/your/documents/*.pdf backend/knowledge_base/

# 2. Run from backend directory
cd backend
python ingest_pdfs_simple.py

# 3. You'll see output like:
# 📄 Found 3 PDF files
# 📖 Loading PDF: policy.pdf
# ✂️ Split into 42 chunks
# 🧠 Generating embeddings...
# 📤 Uploading to Pinecone...
# ✅ Successfully uploaded 42 vectors!
```

---

## 🔧 Customization

Edit `ingest_pdfs_simple.py` to change:

### Chunk Size
```python
documents = chunk_text(text, source=pdf_file.stem, chunk_size=1500)  # Default is 1000
```

### Chunk Overlap
```python
documents = chunk_text(text, source=pdf_file.stem, chunk_size=1000, chunk_overlap=200)  # Default is 100
```

---

## 📦 Free Services Used

| Component | Service | Cost |
|-----------|---------|------|
| PDF Reading | pypdf | FREE |
| Text Splitting | LangChain | FREE |
| Embeddings | HuggingFace | FREE |
| Vector Storage | Pinecone | FREE |

---

## ✨ Features

- ✅ Automatic PDF text extraction
- ✅ Smart text chunking
- ✅ Batch processing
- ✅ Detailed logging
- ✅ Error handling
- ✅ Progress updates
- ✅ 100% FREE (no paid APIs)

---

## 🎯 Next Steps

1. ✅ Place PDFs in `backend/knowledge_base/`
2. ✅ Run `python ingest_pdfs_simple.py`
3. ✅ Wait for completion (varies by PDF size)
4. ✅ Test your chatbot with questions about the PDFs!

---

## ❓ Need Help?

- Check logs in console output
- Verify `.env` file is correct
- Ensure PDFs are valid PDF files
- Check Pinecone dashboard for uploaded vectors

---

**Ready? Let me know when you have PDFs ready! 🚀**
