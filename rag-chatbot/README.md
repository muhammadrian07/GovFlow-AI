# 🚀 RAG Chatbot - Production-Ready Government Policy Assistant

A full-stack **Retrieval-Augmented Generation (RAG)** chatbot system for government policy Q&A with **FastAPI backend** and **React+Vite frontend**. Now with **Grok AI** LLM + **HuggingFace embeddings** - **100% FREE tier!** 🎓

## ✨ Features

- **🤖 RAG Pipeline**: Retrieval-augmented generation with vector embeddings
- **📚 Pinecone Integration**: Vector database for efficient document retrieval (FREE tier)
- **🧠 Grok AI LLM**: Fast, intelligent language model by xAI (FREE API)
- **🌍 HuggingFace Embeddings**: Local embeddings model (NO API key, completely FREE)
- **🎓 Student-Friendly**: $0 cost - perfect for students on a budget
- **🌍 Country Filtering**: Search documents by geographic region
- **⚡ FastAPI Backend**: Async API with comprehensive error handling
- **⚛️ React Frontend**: Modern UI with real-time chat
- **🔐 Secure**: Environment-based configuration, no hardcoded secrets
- **📄 Source Attribution**: View documents used to generate answers
- **🎨 Beautiful UI**: Gradient design, responsive layout
- **📱 Mobile-Friendly**: Works on all devices
- **🔄 Easy LLM Swap**: Use Grok, OpenAI, or compatible APIs

## 📁 Project Structure

```
rag-chatbot/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # Entry point
│   │   ├── core/
│   │   │   └── config.py   # Settings management
│   │   ├── routes/
│   │   │   └── chat.py     # Chat endpoints
│   │   ├── services/
│   │   │   ├── rag_pipeline.py      # Main RAG logic
│   │   │   ├── pinecone_service.py  # Vector DB
│   │   │   └── llm_service.py       # LLM integration
│   │   └── models/
│   │       └── request_models.py    # Pydantic schemas
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                # React + Vite app
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── .gitignore
└── README.md
```

## 🔧 Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **npm or yarn**
- **Pinecone Account** (free tier: 100K vectors)
- **Grok AI API Key** (free at https://console.x.ai)

## 💰 FREE Tier - $0 Cost!

**Perfect for students and learning!** This project uses only FREE services:

| Component | Service | Cost | Why |
|-----------|---------|------|-----|
| LLM (AI Brain) | Grok AI (xAI) | **FREE** | Free API tier available |
| Embeddings | HuggingFace (local) | **FREE** | No API key needed |
| Vector Database | Pinecone | **FREE** | 100K vectors included |
| Backend | FastAPI | **FREE** | Open-source |
| Frontend | React | **FREE** | Open-source |
| **TOTAL COST** | | **$0** | Perfect for students! 🎓 |

### 📚 Documentation for FREE Setup

- **[FREE_TIER_SETUP.md](./FREE_TIER_SETUP.md)** - Complete guide with free API keys and cost breakdown
- **[DIGITAL_OCEAN_DEPLOYMENT.md](./DIGITAL_OCEAN_DEPLOYMENT.md)** - Deploy for FREE with DO student credits

### 🚀 Quick Start

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (includes HuggingFace for FREE embeddings)
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env with your FREE API keys
# PINECONE_API_KEY=your_free_key
# GROK_API_KEY=your_free_key
# EMBEDDINGS_MODEL=all-MiniLM-L6-v2 (FREE, no API key needed!)

# Run backend
python -m uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`


### 2. Frontend Setup

```bash
# Navigate to frontend (new terminal)
cd frontend

# Install dependencies
npm install

# Create .env.local (optional)
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 3. Test the Application

1. Open `http://localhost:5173` in your browser
2. Sign in (mock authentication - any email/password works)
3. Select a country
4. Ask a question about government policies
5. View answers with sources

## 📚 API Documentation

### POST /api/chat

Submit a question and get an answer with sources.

**Request:**
```json
{
  "query": "What are the current tax rates?",
  "country": "USA",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "The current tax rates...",
  "sources": [
    {
      "text": "Relevant excerpt from document",
      "source": "tax_policy_2024.pdf",
      "page": 5
    }
  ],
  "model": "gpt-3.5-turbo"
}
```

### GET /

Health check endpoint

### GET /docs

Interactive API documentation (Swagger UI)

## 🔑 Environment Variables

### Backend (.env)

```env
# Pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=govflow-index
PINECONE_ENVIRONMENT=us-east-1

# Grok AI (LLM)
GROK_API_KEY=your_grok_ai_api_key
LLM_MODEL=grok-1

# OpenAI (for embeddings only)
OPENAI_API_KEY=your_openai_api_key

# App Config
DEBUG=True
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### Frontend (.env.local)

```env
VITE_API_URL=http://localhost:8000/api
```

## 🏗️ Architecture

### Backend Flow

1. **Request**: User sends query + country filter
2. **Embedding**: Query converted to vector using OpenAI embeddings
3. **Retrieval**: Query Pinecone with country filter
4. **Context**: Build prompt with retrieved chunks
5. **Generation**: Grok AI generates answer using context
6. **Response**: Return answer + sources

### Pinecone Vector Schema

```json
{
  "id": "unique-doc-id",
  "values": [0.123, 0.456, ...],
  "metadata": {
    "text": "Document chunk content",
    "source": "filename.pdf",
    "page": 3,
    "country": "USA"
  }
}
```

## 📊 Key Components

### Backend Services

**RAGPipeline**: Orchestrates the entire RAG flow
- Converts queries to embeddings
- Retrieves relevant documents
- Generates answers with LLM
- Formats responses

**PineconeService**: Vector database operations
- Query with metadata filtering
- Upsert documents with embeddings
- Delete vectors

**LLMService**: Language model interaction
- Generate answers from context
- Extract and format sources
- Handle prompt engineering

### Frontend Components

**ChatBox**: Main chat interface
- Message history display
- Input with send button
- Loading states
- Error handling

**Filter**: Country selector
- Dropdown with 8+ countries
- Real-time filter updates

**Message**: Individual message display
- User/assistant messages
- Source attribution
- Timestamps

## 🚢 Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy 'dist' folder to Vercel
# Set environment variables in Vercel dashboard
```

### Backend (Render or Railway)

1. Push code to GitHub
2. Connect repository to Render/Railway
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables
6. Deploy

**Important**: Update CORS_ORIGINS with production URLs

## 🔒 Security Best Practices

✅ Environment variables for all secrets
✅ No hardcoded API keys
✅ CORS middleware configured
✅ Input validation with Pydantic
✅ Error handling without exposing internals
✅ Async endpoints prevent blocking

⚠️ **To do in production**:
- Add authentication (JWT/OAuth)
- Implement rate limiting
- Add request logging
- Use HTTPS
- Set appropriate CORS origins
- Add monitoring/alerting

## 🧪 Testing

### Backend
```bash
cd backend
pip install pytest
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 📝 Customization

### Use Grok AI (Recommended)

1. Get Grok API key from https://console.x.ai/
2. Add to `backend/.env`:
   ```env
   GROK_API_KEY=your_grok_key
   LLM_MODEL=grok-1
   ```
3. Keep OpenAI API key for embeddings
4. See [GROK_SETUP.md](./GROK_SETUP.md) for detailed setup

### Add New Countries

Edit [Filter.jsx](frontend/src/components/Filter.jsx):
```jsx
const countries = [
  'USA',
  'UK',
  'Canada',
  'YourCountry'  // Add here
]
```

### Change LLM Provider

Edit [config.py](backend/app/core/config.py) and [llm_service.py](backend/app/services/llm_service.py):
```python
# Use Grok instead of OpenAI
# llm = Grok(api_key=api_key)
```

### Customize Prompts

Edit [rag_pipeline.py](backend/app/services/rag_pipeline.py):
```python
prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template="Your custom prompt here..."
)
```

## 🐛 Troubleshooting

### Backend won't start
- Check Python version (3.9+)
- Verify .env file exists and has API keys
- Check port 8000 is not in use

### Frontend won't connect to backend
- Ensure backend is running on 8000
- Check VITE_API_URL in .env.local
- Check CORS_ORIGINS in backend .env

### No results from Pinecone
- Verify API key is correct
- Check index name matches
- Ensure documents are uploaded to Pinecone
- Verify country filter matches document metadata

### API rate limiting
- Check OpenAI quota
- Check Pinecone quota
- Implement request throttling in production

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pinecone Docs](https://docs.pinecone.io/)
- [LangChain Docs](https://python.langchain.com/)
- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)

## 📄 License

MIT License - Feel free to use for personal and commercial projects

## 🤝 Contributing

Contributions welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ✉️ Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review code comments for implementation details

---

**Built with ❤️ for government policy research**
