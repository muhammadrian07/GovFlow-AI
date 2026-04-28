# 🏛️ Government Policy RAG Chatbot

A production-ready **Retrieval-Augmented Generation (RAG) chatbot** that answers government policy questions using intelligent document retrieval and AI-powered responses.

---

## ✨ Features

- **📚 Intelligent Document Retrieval**: Vector embeddings + semantic search via Pinecone
- **🤖 Hybrid AI System**: Uses document context when available, falls back to LLM for general questions
- **🌍 Multi-Country Support**: Filter results by country/region (Pakistan, USA, etc.)
- **👤 User Authentication**: Sign up, login, persistent sessions
- **📄 PDF Ingestion**: Automatically process and chunk policy documents
- **📖 Source References**: See which documents answered your question
- **⚡ Free Tier Stack**: HuggingFace embeddings, Groq LLM, Pinecone (all free)
- **🔒 Country-Aware Responses**: Rejects questions about different countries than selected filter

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10)
- **Vector DB**: Pinecone (free tier - 100K vectors)
- **LLM**: Groq (free tier)
- **Embeddings**: HuggingFace all-MiniLM-L6-v2 (local, free)
- **PDF Processing**: pypdf + LangChain

### Frontend
- **Framework**: React + Vite
- **Authentication**: localStorage
- **HTTP Client**: Axios

### Infrastructure
- **Backend Deployment**: Digital Ocean (App Platform)
- **Frontend Deployment**: Vercel

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn
- API Keys (free):
  - [Groq API Key](https://console.groq.com)
  - [Pinecone API Key](https://www.pinecone.io)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd govflow_ai/rag-chatbot
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file
   cp .env.example .env
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

---

## ⚙️ Configuration

### Backend `.env` File

```env
# Groq LLM (Free tier)
GROQ_API_KEY=gsk_your_api_key_here
LLM_MODEL=llama-3.1-8b-instant

# Pinecone Vector Database
PINECONE_API_KEY=pcsk_your_api_key_here
PINECONE_INDEX=govflowai
PINECONE_ENVIRONMENT=us-east-1

# Embeddings
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

### Frontend `.env` File

```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

---

## 🏃 Running Development Servers

### Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
✅ Backend running at: http://localhost:8000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
✅ Frontend running at: http://localhost:5173

---

## 📚 How to Use

### 1. Create Account
- Go to http://localhost:5173
- Click "Sign up"
- Enter name, email, password
- Account is saved to localStorage (development only)

### 2. Select Country
- Choose from dropdown: Pakistan, USA, etc.
- Filter applies to all questions

### 3. Ask Questions
- **Policy Questions**: "What are commercial zone regulations in Lahore?"
  - ✅ Returns answers from documents with sources

- **General Questions**: "Tell me about yourself"
  - ✅ Falls back to LLM (no sources)

- **Out-of-Scope**: "What's the weather?"
  - ❌ Rejected as non-policy question

### 4. View Sources
- Sources shown below each answer
- Indicates which document answered your question

---

## 📄 PDF Ingestion

### Add New PDFs
1. Place PDF files in `backend/knowledge_base/`
2. Run ingestion script:
   ```bash
   cd backend
   python ingest_pdfs_simple.py
   ```
3. New vectors uploaded to Pinecone automatically

### Automatic Country Detection
- **Naming Convention**: 
  - `*LDA*.pdf` → Tagged as "Pakistan"
  - `*USA*.pdf` → Tagged as "USA"
  - Other files → Tagged as "GLOBAL"

---

## 🔌 API Endpoints

### POST `/api/chat`
Query the chatbot with a question.

**Request:**
```json
{
  "query": "What are the building regulations?",
  "country": "Pakistan",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Building regulations include...",
  "sources": [
    {
      "source": "2.LDA Landuse Rules_2020",
      "text": "Building regulations excerpt...",
      "page": null
    }
  ],
  "model": "llama-3.1-8b-instant (RAG Mode)"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 🧪 Testing

### Test Legal Questions (Pakistan)
1. Select "Pakistan"
2. Ask: "What are the amendments in the LDA Building and Zoning Regulations for 2019?"
   - Expected: ✅ Shows sources from LDA PDFs

### Test General Questions
1. Ask: "How can you help me?"
   - Expected: ✅ LLM response, no sources

### Test Out-of-Domain
1. Ask: "What's the weather?"
   - Expected: ❌ Rejected as non-policy

### Test Country Filter
1. Select "USA"
2. Ask: "What are LDA regulations?"
   - Expected: ❌ "You've selected USA filter, but asked about Pakistan"

---

## 🐳 Docker Deployment

### Backend
```bash
cd backend
docker build -t govflow-backend .
docker run -p 8000:8000 --env-file .env govflow-backend
```

### Frontend
```bash
cd frontend
docker build -t govflow-frontend .
docker run -p 3000:3000 govflow-frontend
```

---

## ☁️ Production Deployment

### Digital Ocean (Backend)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Production ready"
   git push origin main
   ```

2. **Create App on Digital Ocean**
   - Connect GitHub repo
   - Set build command: `cd backend && pip install -r requirements.txt`
   - Set run command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8080`
   - Set environment variables (from `.env`)
   - Deploy

3. **Estimated Cost**: ~$5-12/month (App Platform)

### Vercel (Frontend)

1. **Create Vercel Project**
   - Import from GitHub
   - Set root directory: `frontend`
   - Build command: `npm run build`
   - Output: `dist`

2. **Environment Variables**
   - `VITE_API_URL=<your-digital-ocean-backend-url>`

3. **Deploy** - automatic on git push

---

## 🏗️ Architecture

```
User Browser (Frontend - Vercel)
    ↓ (HTTP REST API)
    ↓
FastAPI Backend (Digital Ocean)
    ↓
RAG Pipeline:
    ├→ HuggingFace (embed query)
    ├→ Pinecone (retrieve vectors)
    └→ Groq LLM (generate answer)
    ↓
Returns: Answer + Sources
```

### How RAG Works

1. **User asks question** → Frontend sends to backend
2. **Embed query** → HuggingFace generates 384-dim vector (free, local)
3. **Retrieve documents** → Pinecone searches with country filter
4. **Smart filtering** → Only uses docs with relevance score ≥ 0.5
5. **Generate answer** → Groq LLM with document context (free tier)
6. **Return response** → Answer + source references

### Two Modes

- **RAG Mode**: Documents found + score ≥ 0.5
  - Model: "llama-3.1-8b-instant (RAG Mode)"
  - Sources: Shown
  
- **General Mode**: No documents OR score < 0.5
  - Model: "llama-3.1-8b-instant (General Mode)"
  - Sources: Empty
  - Still country-filtered

---

## 🔐 Security Notes

### Current (Development)
- ⚠️ Passwords stored in plain text (localStorage)
- ⚠️ No rate limiting
- ⚠️ No API authentication

### For Production
- ✅ Add PostgreSQL database for users
- ✅ Hash passwords with bcrypt
- ✅ Add JWT authentication
- ✅ Implement rate limiting
- ✅ Use HTTPS only
- ✅ Add CORS properly configured
- ✅ Store API keys securely

---

## 📊 Free Tier Limits

| Service | Free Tier | Limit |
|---------|-----------|-------|
| Pinecone | Vector DB | 100,000 vectors |
| Groq | LLM | High rate limit |
| HuggingFace | Embeddings | Local (unlimited) |
| Digital Ocean | Backend | $5/month |
| Vercel | Frontend | Unlimited |

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Try different port
uvicorn app.main:app --port 8001
```

### Frontend API errors
- Check `.env` has correct backend URL
- Verify backend is running
- Check CORS settings in `app/main.py`

### No documents retrieved
- Verify PDFs in `backend/knowledge_base/`
- Run: `python ingest_pdfs_simple.py`
- Check Pinecone dashboard for vectors

### Wrong answers
- Check if question matches document content
- Verify country filter matches question topic
- Try more specific question phrasing

---

## 📝 Project Structure

```
govflow_ai/rag-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── core/config.py       # Environment config
│   │   ├── models/
│   │   │   └── request_models.py # Pydantic models
│   │   ├── routes/
│   │   │   └── chat.py          # /api/chat endpoint
│   │   └── services/
│   │       ├── embeddings_service.py  # HuggingFace
│   │       ├── pinecone_service.py    # Vector DB
│   │       ├── llm_service.py         # Groq LLM
│   │       └── rag_pipeline.py        # RAG orchestration
│   ├── knowledge_base/          # PDF storage
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   └── Chat.jsx
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Filter.jsx
│   │   │   └── Message.jsx
│   │   └── services/
│   │       └── api.js           # API client
│   ├── .env.example
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 📧 Support

For issues or questions:
1. Check **Troubleshooting** section above
2. Review API endpoints documentation
3. Check backend logs: `uvicorn` output
4. Verify `.env` configuration

---

## 📄 License

MIT License - Feel free to use and modify

---

## 🎯 Next Steps

- [ ] Add database for persistent user storage
- [ ] Implement JWT authentication
- [ ] Add chat history per user
- [ ] Deploy to Digital Ocean
- [ ] Deploy to Vercel
- [ ] Add rate limiting
- [ ] Add admin dashboard for PDF management

---

**Last Updated**: April 28, 2026  
**Version**: 1.0.0 - Production Ready
