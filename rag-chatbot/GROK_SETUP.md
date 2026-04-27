# � Complete GROK + HuggingFace FREE Setup

This guide explains the final setup: **Grok AI LLM** + **HuggingFace Embeddings** (100% FREE).

## 📋 Architecture

| Component | Service | Cost |
|-----------|---------|------|
| **LLM** | Grok AI (grok-1) | FREE (xAI) |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | FREE (local) |
| **Vector DB** | Pinecone | FREE (100K vectors) |
| **Integration** | LangChain | FREE (open-source) |

### Why This Stack?
- ✅ 100% FREE - No paid services
- ✅ Open-source where possible
- ✅ Fast local embeddings (no API latency)
- ✅ Grok has free API tier
- ✅ Perfect for students

## 🔑 Getting Grok API Key

### Step 1: Create Account
1. Go to https://console.x.ai/
2. Sign up with your email
3. Verify your email
4. Complete profile

### Step 2: Generate API Key
1. Navigate to API Settings
2. Click "Create API Key"
3. Copy the key immediately (won't show again)
4. Label it: `rag-chatbot`

### Step 3: Model Name
- **Model**: `grok-1`
- **Endpoint**: `https://api.x.ai/v1/chat/completions`
- **Free Tier**: Yes, rate limited

## 📦 HuggingFace Embeddings (Already Included!)

**No API key needed!** Embeddings run locally using:
- Model: `all-MiniLM-L6-v2` (recommended)
- Size: ~22MB
- Downloads automatically on first use
- Runs offline

Other free models available:
- `all-mpnet-base-v2` - Better quality, slightly slower
- `paraphrase-MiniLM-L6-v2` - Good for policy docs

## 🔧 Configuration (.env)

```env
# Grok LLM (FREE - get from console.x.ai)
GROK_API_KEY=xai-your_key_here
LLM_MODEL=grok-1

# Pinecone Vector DB (FREE - 100K vectors)
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX=starter-index
PINECONE_ENVIRONMENT=us-east-1

# HuggingFace Embeddings (FREE - runs locally, NO API KEY)
EMBEDDINGS_PROVIDER=huggingface
EMBEDDINGS_MODEL=all-MiniLM-L6-v2

# App Config
DEBUG=True
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## ✅ Quick Start

```bash
# 1. Navigate to backend
cd backend

# 2. Create/update .env with above values

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
uvicorn app.main:app --reload

# 5. Test it
curl http://localhost:8000/health
```

## 📊 Cost Breakdown

| Service | Original | Current |
|---------|----------|---------|
| LLM | $20-100/mo | FREE |
| Embeddings | $0.02-1/K tokens | FREE |
| Vector DB | $72-500/mo | FREE |
| **TOTAL** | **$92-600/mo** | **$0** ✅ |

## 🎓 Student Resources

- [FREE_TIER_SETUP.md](./FREE_TIER_SETUP.md) - Complete student guide
- [DIGITAL_OCEAN_DEPLOYMENT.md](./DIGITAL_OCEAN_DEPLOYMENT.md) - Free deployment

## ⚠️ Grok Free Tier Limits

- Rate limited (check xAI docs for specifics)
- Great for development/learning
- Upgrade anytime if needed

## 🚀 Next Steps

1. Get Grok API key from https://console.x.ai/
2. Set `.env` file
3. Install dependencies
4. Run: `python ingest_pdfs_simple.py` to upload PDFs
5. Start chatting!

---

**Everything is FREE! 🎉**


**Key packages for Grok**:
- `httpx` - HTTP client for Grok API
- `openai` - For embeddings
- `pinecone-client` - Vector database
- `langchain` - LLM framework

### 2. Verify API Keys

Test your Grok API key:

```python
import httpx

def test_grok_api():
    api_key = "your_grok_api_key"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-1",
        "messages": [
            {"role": "user", "content": "Hello"}
        ]
    }
    
    with httpx.Client() as client:
        response = client.post(
            "https://api.x.ai/v1/chat/completions",
            json=payload,
            headers=headers
        )
        print(response.json())

test_grok_api()
```

## 📊 API Flow

```
User Query
    ↓
Frontend (React)
    ↓
Backend API POST /api/chat
    ↓
RAG Pipeline
    ├─ Embed Query (OpenAI API)
    ├─ Query Pinecone
    ├─ Retrieve Documents
    └─ Call Grok API (LLM)
        ↓
    Grok Response
        ↓
Format Answer + Sources
    ↓
Return to Frontend
    ↓
Display to User
```

## 🔄 How Grok Integration Works

### 1. LLM Service

The `LLMService` class now makes direct HTTP calls to Grok:

```python
def _call_grok_api(self, system_message, user_message):
    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-1",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    response = httpx.post(
        "https://api.x.ai/v1/chat/completions",
        json=payload,
        headers=headers
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 2. Request Format

**Request to Grok API**:
```json
{
  "model": "grok-1",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful government policy assistant..."
    },
    {
      "role": "user",
      "content": "Context: [...]\nQuestion: What are tax deductions?\nAnswer:"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

**Response from Grok API**:
```json
{
  "choices": [
    {
      "message": {
        "content": "Tax deductions are expenses that reduce your taxable income..."
      }
    }
  ]
}
```

## ⚡ Running the Application

### With Grok

```bash
# Backend
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm run dev
```

**Logs will show**:
```
✅ Grok LLM service initialized with model: grok-1
✅ RAG Pipeline initialized (Grok LLM + OpenAI Embeddings)
```

## 📊 Cost Comparison

| Service | Cost |
|---------|------|
| Grok API | Varies (check pricing) |
| OpenAI Embeddings | $0.0001 per 1K tokens |
| Pinecone | Free tier (1 pod) |
| **Total** | **Low** |

### Cost Optimization Tips
1. Cache embeddings locally
2. Reuse embeddings for similar queries
3. Monitor token usage
4. Use smaller contexts when possible

## 🐛 Troubleshooting

### "Invalid API Key" Error

```
Grok API HTTP error: 401 Unauthorized
```

**Solution**:
1. Verify API key is correct
2. Check it's not expired
3. Ensure it's in backend/.env
4. Restart backend server

### "Model Not Found" Error

```
Grok API HTTP error: 404 Not Found
```

**Solution**:
- Use `grok-1` as model name (not `grok-2`, `grok-3`, etc.)
- Check latest available models at console.x.ai

### Slow Response Time

**Causes**:
- Network latency
- Grok API rate limiting
- Large context chunks
- Token limit exceeded

**Solutions**:
1. Reduce top_k in frontend (retrieve fewer documents)
2. Reduce context chunk size
3. Use caching
4. Check Grok API status

### "Token Limit Exceeded"

**Solution**:
- Reduce max_tokens in llm_service.py
- Shorter context chunks
- Shorter user queries

## 🔒 Security

### Keep Your Keys Safe

```bash
# ✅ DO THIS
export GROK_API_KEY="your_key"
cat backend/.env  # Don't commit!

# ❌ DON'T DO THIS
grok_api_key = "your_key"  # In code
git commit .env            # Commit secrets
```

### .env File Protection

```bash
# Add to .gitignore (already done)
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

## 📈 Monitoring Usage

### Check Grok Usage

Log into console.x.ai to view:
- API call count
- Token usage
- Estimated costs
- Rate limits

### Enable Backend Logging

In `backend/app/main.py`:
```python
logging.basicConfig(level=logging.INFO)
```

View logs to see:
```
Generated answer for query: What are...
Grok API call successful
```

## 🚢 Deployment with Grok

### Render / Railway Setup

Set environment variables:
```
GROK_API_KEY=your_production_key
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
LLM_MODEL=grok-1
```

### Docker Setup

```yaml
services:
  backend:
    environment:
      - GROK_API_KEY=${GROK_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
```

## 🎯 Next Steps

1. ✅ Get Grok API key
2. ✅ Get OpenAI API key (embeddings)
3. ✅ Update .env file
4. ✅ Install dependencies: `pip install -r requirements.txt`
5. ✅ Start backend: `python -m uvicorn app.main:app --reload`
6. ✅ Test at http://localhost:8000/docs
7. ✅ Try a query with http://localhost:5173

## 📚 API Documentation

### POST /api/chat

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital gains tax rate?",
    "country": "USA",
    "top_k": 5
  }'
```

**Response**:
```json
{
  "answer": "The capital gains tax rate varies...",
  "sources": [
    {
      "text": "Capital gains...",
      "source": "tax_guide.pdf",
      "page": 5
    }
  ],
  "model": "grok-1"
}
```

## 🔗 Resources

- **Grok API Docs**: https://docs.x.ai/ (or console.x.ai)
- **xAI Website**: https://x.ai/
- **Grok Console**: https://console.x.ai/
- **OpenAI API**: https://platform.openai.com/
- **Pinecone Docs**: https://docs.pinecone.io/

## ✅ Checklist

- [ ] Created Grok account
- [ ] Generated Grok API key
- [ ] Generated OpenAI API key
- [ ] Updated backend/.env
- [ ] Installed dependencies
- [ ] Tested Grok API connection
- [ ] Started backend server
- [ ] Started frontend
- [ ] Tested chat endpoint
- [ ] Ready for deployment!

---

**Status**: ✅ Grok AI Configured

Your RAG Chatbot is now using Grok AI for LLM generation!
