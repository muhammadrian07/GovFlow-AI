# 🎓 DOCUMENTATION - RAG Chatbot

## System Architecture

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │ HTTP/WS
       ▼
┌──────────────────────┐
│  React + Vite        │
│  Frontend            │
│  (Port 5173)         │
└──────┬───────────────┘
       │ /api/chat
       ▼
┌──────────────────────┐
│  FastAPI Backend     │
│  (Port 8000)         │
└──────┬───────────────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
    ┌──────────┐    ┌──────────┐
    │ Pinecone │    │ OpenAI   │
    │ (Vector  │    │ (LLM)    │
    │  DB)     │    │          │
    └──────────┘    └──────────┘
```

## RAG Pipeline Explained

### Step 1: User Input
User enters a question like "What are tax deductions?"

### Step 2: Embedding Generation
```python
# Query converted to vector
query = "What are tax deductions?"
embedding = embeddings.embed_query(query)
# Result: [0.123, 0.456, 0.789, ...]
```

### Step 3: Vector Search
```python
# Query Pinecone with country filter
results = pinecone.query(
    vector=embedding,
    top_k=5,
    filter={"country": {"$eq": "USA"}}
)
```

### Step 4: Context Preparation
```python
context = """
Tax Deductions are expenses you can subtract from income:

1. Standard Deduction: $13,850 (single)
2. Itemized Deductions: Medical, mortgage, etc.
3. Business Deductions: Equipment, supplies
"""
```

### Step 5: Prompt Construction
```
You are a tax expert. Answer ONLY from the context.

Context:
{context}

Question: What are tax deductions?

Answer:
```

### Step 6: LLM Generation
```python
answer = llm.generate(prompt)
# Returns detailed answer based on context
```

### Step 7: Response with Sources
```json
{
  "answer": "Tax deductions are...",
  "sources": [
    {
      "text": "Tax Deductions are expenses...",
      "source": "tax_guide_2024.pdf",
      "page": 5
    }
  ]
}
```

## Code Organization

### Backend Structure

```
backend/app/
├── main.py
│   └── FastAPI application setup
│       - Lifespan management
│       - CORS middleware
│       - Service initialization
│
├── core/config.py
│   └── Environment configuration
│       - Load .env variables
│       - Pydantic settings
│       - Global config access
│
├── models/request_models.py
│   └── Data validation models
│       - ChatRequest
│       - ChatResponse
│       - SourceReference
│
├── services/
│   ├── rag_pipeline.py
│   │   └── Main orchestrator
│   │       - Embedding → Retrieval → Generation
│   │       - Async query processing
│   │       - Error handling
│   │
│   ├── pinecone_service.py
│   │   └── Vector database
│   │       - Query with filters
│   │       - Upsert documents
│   │       - Delete operations
│   │
│   └── llm_service.py
│       └── Language model
│           - Answer generation
│           - Prompt engineering
│           - Source extraction
│
└── routes/chat.py
    └── API endpoints
        - POST /api/chat
        - GET /health
```

### Frontend Structure

```
frontend/src/
├── main.jsx
│   └── React entry point
│
├── App.jsx
│   └── Main app component
│       - Auth state management
│       - Route handling
│       - Page switching
│
├── pages/
│   ├── Login.jsx - Mock authentication
│   ├── Signup.jsx - User registration (mock)
│   └── Chat.jsx - Main chat interface
│
├── components/
│   ├── ChatBox.jsx - Message display & input
│   ├── Message.jsx - Individual messages
│   └── Filter.jsx - Country selector
│
└── services/
    └── api.js - Axios API client
        - Request interceptors
        - Response interceptors
        - Error handling
```

## Key Concepts

### Vector Embeddings

Embeddings convert text to numbers:
```
"What is tax?" → [0.12, 0.34, 0.56, -0.89, ...]
```

Two similar questions have similar vectors (close in space).

### Metadata Filtering

Each vector stores metadata for filtering:
```json
{
  "text": "Tax is mandatory...",
  "country": "USA",
  "source": "tax_guide.pdf",
  "page": 1
}
```

### Retrieval

Find top-k similar documents:
```python
# Find 5 documents most similar to query
# And matching country filter
results = pinecone.query(
    vector=query_embedding,
    top_k=5,
    filter={"country": "USA"}
)
```

### Generation

Use context to answer:
```
LLM receives:
1. Question: "How do I deduct taxes?"
2. Context: [Retrieved document chunks]
3. Instruction: "Answer ONLY from context"

Returns: Detailed answer
```

## Common Patterns

### Error Handling

```python
try:
    # Attempt operation
    result = pinecone.query(...)
except Exception as e:
    logger.error(f"Error: {str(e)}")
    # Return user-friendly error
    raise HTTPException(status_code=500, detail="...")
```

### Async Processing

```python
async def chat(request: ChatRequest):
    # Non-blocking operations
    embedding = await pipeline.embed_query(request.query)
    documents = await pipeline.retrieve_documents(embedding)
    answer = await pipeline.generate_answer(documents)
    return response
```

### Dependency Injection

```python
# Define dependency
def get_pipeline() -> RAGPipeline:
    return global_pipeline

# Use in endpoint
@app.post("/chat")
async def chat(pipeline: RAGPipeline = Depends(get_pipeline)):
    # Function receives pipeline automatically
    pass
```

## Configuration Management

### Environment Variables

Located in `.env` file:
```
PINECONE_API_KEY=...
OPENAI_API_KEY=...
LLM_MODEL=gpt-3.5-turbo
DEBUG=True
```

### Settings Class

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pinecone_api_key: str
    openai_api_key: str
    debug: bool = True
    
    class Config:
        env_file = ".env"
```

### Global Access

```python
from app.core.config import settings

# Anywhere in code
api_key = settings.pinecone_api_key
debug_mode = settings.debug
```

## Performance Optimization

### Caching

```python
# Cache embeddings for common queries
cache = {}
if query in cache:
    return cache[query]
embedding = generate_embedding(query)
cache[query] = embedding
```

### Batch Processing

```python
# Process multiple queries at once
batch_embeddings = embeddings.embed_documents(queries)
```

### Connection Pooling

```python
# Reuse database connections
pinecone_client = Pinecone(api_key=key)  # Reuses internally
```

## Testing Strategy

### Backend Tests

```python
import pytest

def test_chat_endpoint():
    response = client.post("/api/chat", json={
        "query": "test",
        "country": "USA"
    })
    assert response.status_code == 200
    assert "answer" in response.json()
```

### Frontend Tests

```javascript
import { render, screen } from '@testing-library/react'
import Chat from './Chat'

test('renders chat component', () => {
    render(<Chat />)
    expect(screen.getByText(/Government Policy/i)).toBeInTheDocument()
})
```

## Security Considerations

### API Key Protection

✅ Store in `.env` file
✅ Use environment variables
✅ Never commit to Git
❌ Don't hardcode
❌ Don't log

### CORS Configuration

```python
# Whitelist specific origins
CORS_ORIGINS = [
    "https://yourdomain.com",  # Production
    "http://localhost:5173",    # Development
]
```

### Input Validation

```python
# Pydantic validates automatically
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    country: str = Field(...)
```

### Error Messages

```python
# Don't expose internals
raise HTTPException(
    status_code=500,
    detail="An error occurred"  # Generic
    # NOT: detail=f"Database error: {specific_error}"
)
```

## Monitoring & Debugging

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing query...")
logger.error("Error occurred", exc_info=True)
```

### Debug Mode

```python
# In development
DEBUG=True

# Shows detailed error pages
# Enables auto-reload
# Shows logs
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive documentation.

## Troubleshooting Guide

### Issue: No results from Pinecone

**Check:**
1. API key is correct
2. Index name matches
3. Documents uploaded
4. Country filter exists

```python
# Verify data exists
results = pinecone.query(vector=..., top_k=10)  # No filter
```

### Issue: Slow responses

**Check:**
1. Pinecone latency
2. OpenAI latency
3. Network issues
4. Database size

```python
# Time individual steps
start = time.time()
embedding = generate_embedding(query)
print(f"Embedding: {time.time() - start}s")
```

### Issue: CORS errors

**Check:**
1. Backend CORS configuration
2. Frontend API URL
3. Browser console errors

```python
# Verify CORS middleware
@app.middleware("http")
async def check_cors(request, call_next):
    # Check headers
    origin = request.headers.get("origin")
```

## Advanced Customization

### Custom Prompts

Edit `rag_pipeline.py`:
```python
prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template="Your custom template..."
)
```

### Alternative LLMs

```python
# Use Grok instead
from langchain_community.llms import GrokLLM

llm = GrokLLM(api_key=api_key)
```

### Custom Embeddings

```python
# Use different embedding model
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="...")
```

---

**For more info, see code comments and docstrings in each file.**
