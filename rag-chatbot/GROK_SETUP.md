# 🔑 GROK API SETUP - RAG Chatbot

This guide explains how to set up and use **Grok AI API** instead of OpenAI for the RAG Chatbot.

## 🔄 What Changed?

| Component | Before | Now |
|-----------|--------|-----|
| **LLM** | OpenAI (gpt-3.5-turbo) | Grok AI (grok-1) |
| **Embeddings** | OpenAI | OpenAI (kept for embeddings) |
| **API Provider** | OpenAI | xAI (Grok) |

### Why Grok?
- ✅ Free tier available
- ✅ Fast inference
- ✅ Real-time knowledge cutoff
- ✅ Good for government policy content
- ✅ Lower latency

## 📋 Getting Grok API Key

### Step 1: Create Account
1. Go to https://console.x.ai/ or https://grok.com/
2. Sign up with your email
3. Verify your email address
4. Complete profile setup

### Step 2: Generate API Key
1. Navigate to API settings
2. Click "Create API Key" or "Generate Key"
3. Copy the API key (save it securely)
4. Give it a descriptive name: `rag-chatbot`

### Step 3: Note the Model Name
- **Model ID**: `grok-1` (default)
- API Endpoint: `https://api.x.ai/v1/chat/completions`

## 🔑 Getting OpenAI API Key (for Embeddings)

You still need OpenAI API key for generating embeddings:

1. Go to https://platform.openai.com/api/keys
2. Create a new secret key
3. Copy the key
4. Save it securely

## ⚙️ Configuration

### Update .env File

In `backend/.env`, set:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=your_index_name
PINECONE_ENVIRONMENT=us-east-1

# Grok AI (LLM)
GROK_API_KEY=your_grok_api_key_here
LLM_MODEL=grok-1

# OpenAI (Embeddings only)
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDINGS_PROVIDER=openai

# Application
DEBUG=True
CORS_ORIGINS=["http://localhost:5173"]
```

## 🚀 Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

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
