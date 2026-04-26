# 🚀 SETUP GUIDE - RAG Chatbot

This guide walks you through setting up the RAG Chatbot system step-by-step.

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.9 or higher**
   ```bash
   python --version
   ```

2. **Node.js 18+ and npm**
   ```bash
   node --version
   npm --version
   ```

3. **Git** (optional, for version control)

4. **API Accounts:**
   - Pinecone (https://www.pinecone.io) - For vector database
   - OpenAI (https://platform.openai.com) - For embeddings & LLM
   - Or Grok (https://grok.com) - Alternative LLM

## 🔑 Step 1: Get API Keys

### Pinecone API Key
1. Go to https://www.pinecone.io
2. Sign up for a free account
3. Create a new index or use existing
4. Copy your API key from the dashboard
5. Note your index name and environment

### OpenAI API Key
1. Go to https://platform.openai.com/api/keys
2. Create a new secret key
3. Copy the key (save it, you won't see it again)
4. Set up billing in your account

## 📦 Step 2: Backend Setup

### 2.1 Navigate to Backend Directory
```bash
cd backend
```

### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pinecone - Vector database client
- LangChain - LLM framework
- OpenAI - LLM provider

### 2.4 Create Environment File
```bash
cp .env.example .env
```

### 2.5 Edit .env with Your Keys

Open `backend/.env` in a text editor and fill in your credentials:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=your_index_name
PINECONE_ENVIRONMENT=us-east-1

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-3.5-turbo

# Application Configuration
DEBUG=True
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 2.6 Start Backend Server

```bash
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **Backend is ready!** Visit http://localhost:8000/docs to see API documentation.

## ⚛️ Step 3: Frontend Setup

### 3.1 Open New Terminal and Navigate

```bash
cd frontend
```

### 3.2 Install Dependencies

```bash
npm install
```

This installs React, Vite, Axios, etc.

### 3.3 Create Environment File (Optional)

```bash
cp .env.example .env.local
```

The default configuration should work, but you can customize:
```
VITE_API_URL=http://localhost:8000/api
```

### 3.4 Start Development Server

```bash
npm run dev
```

You should see:
```
  ➜  Local:   http://localhost:5173/
```

✅ **Frontend is ready!** Visit http://localhost:5173 in your browser.

## 🧪 Step 4: Test the Application

1. **Open Frontend**: Visit http://localhost:5173
2. **Login**: Use any email/password (mock auth)
   - Email: `test@example.com`
   - Password: `password123`
3. **Select Country**: Choose from the dropdown
4. **Ask a Question**: Try "What are government policies?"
5. **View Answer**: You'll see the response with sources

## ✨ What Happens Behind the Scenes

1. Your question is sent to the backend
2. Question is converted to a vector embedding
3. Backend queries Pinecone for similar documents from your country
4. Retrieved documents are passed to OpenAI
5. OpenAI generates an answer based on the context
6. Frontend displays the answer with source citations

## 🔄 Workflow

Keep both servers running:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # (or venv\Scripts\activate on Windows)
python -m uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## 🛠️ Useful Commands

### Backend

| Command | Purpose |
|---------|---------|
| `pip install -r requirements.txt` | Install Python packages |
| `pip freeze > requirements.txt` | Update requirements |
| `python -m uvicorn app.main:app --reload` | Start dev server |
| `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000` | Start on all interfaces |

### Frontend

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies |
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |

## 📝 Project Structure Reference

```
rag-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # Entry point
│   │   ├── routes/
│   │   │   └── chat.py          # API endpoints
│   │   ├── services/
│   │   │   ├── rag_pipeline.py  # RAG logic
│   │   │   ├── pinecone_service.py
│   │   │   └── llm_service.py
│   │   ├── models/
│   │   │   └── request_models.py
│   │   └── core/
│   │       └── config.py        # Settings
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                     # (Don't commit this!)
│
├── frontend/
│   ├── src/
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   ├── services/            # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.local              # (Don't commit this!)
│
├── .gitignore
└── README.md
```

## 🐛 Common Issues & Solutions

### Backend fails to start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Frontend won't connect to backend

**Error:** `Failed to fetch` or CORS error

**Solution:**
1. Make sure backend is running: `http://localhost:8000`
2. Check CORS_ORIGINS in `backend/.env`:
   ```env
   CORS_ORIGINS=["http://localhost:5173"]
   ```
3. Restart backend after changing .env

### No results from Pinecone

**Solution:**
1. Verify API key is correct
2. Check index name in backend/.env
3. Ensure documents are uploaded to Pinecone
4. Verify country name matches document metadata

### Pinecone "No free trial available"

**Solution:** Upgrade Pinecone account or use a new project

## 🚀 Next Steps

1. **Upload Documents**: Add your policy documents to Pinecone
2. **Customize UI**: Modify styles in `frontend/src/` files
3. **Add Countries**: Edit [Filter.jsx](../frontend/src/components/Filter.jsx)
4. **Deploy**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
5. **Add Features**: Integrate authentication, history, etc.

## 📚 Additional Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Pinecone**: https://docs.pinecone.io/
- **LangChain**: https://python.langchain.com/
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/

## 💡 Tips

1. **Keep API keys private**: Never commit .env files
2. **Use different indexes**: One for development, one for production
3. **Monitor costs**: Track API usage in OpenAI/Pinecone dashboards
4. **Test incrementally**: Start with one country/document type
5. **Read the logs**: They tell you what's happening

---

**Questions?** Check the code comments for detailed explanations.
