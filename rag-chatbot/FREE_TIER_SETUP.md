# 🎓 FREE Tier RAG Chatbot - Student Guide

This chatbot uses **100% free services** - perfect for students with zero budget! 💰

## Total Cost: **$0** 🎉

---

## 📋 Free Services Used

| Service | Purpose | Free Tier | Cost |
|---------|---------|-----------|------|
| **HuggingFace** | Text Embeddings | all-MiniLM-L6-v2 model (local) | $0 |
| **Grok AI** | LLM/AI Brain | Free API tier (xAI) | $0 |
| **Pinecone** | Vector Database | 1 pod, 100K vectors | $0 |
| **FastAPI** | Backend Server | Open-source | $0 |
| **React** | Frontend UI | Open-source | $0 |
| **Digital Ocean** | Deployment | Student Program ($50-200/mo credit) | ~$0 |
| **Vercel** | Frontend Hosting | Free tier | $0 |
| **GitHub** | Code Repository | Free public repos | $0 |

---

## 🚀 Quick Start (5 minutes)

### 1. Get Free API Keys

#### Grok AI (LLM - FREE)
```bash
# Visit: https://console.x.ai
# Sign up with email
# Get free API key (no credit card needed!)
# Note: Free tier has usage limits
```

#### Pinecone (Vector DB - FREE)
```bash
# Visit: https://www.pinecone.io
# Sign up free
# Create starter index (1 pod, 100K vectors)
# Get API key and environment
```

### 2. Clone & Setup Backend
```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit .env with your keys
# GROK_API_KEY=your_key_here
# PINECONE_API_KEY=your_key_here

# Install Python dependencies (uses free packages)
pip install -r requirements.txt

# Run backend server
uvicorn app.main:app --reload
```

### 3. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Test Locally
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## 💡 Why These Services Are Free

### HuggingFace Embeddings
- **Local models** - runs on your machine
- **No API key** - no authentication needed
- **No usage limits** - unlimited free embeddings
- **Model sizes**: 22-438 MB (fits in memory)

### Grok AI
- **Free API tier** available through xAI
- **Learning/Development** tier with reasonable limits
- **No credit card** required initially
- **Pay-as-you-go** if you scale (but you can start free)

### Pinecone
- **Free tier**: 
  - 1 pod (small vector storage)
  - 100K vectors max
  - Great for small-medium datasets
  - Perfect for learning

### Digital Ocean (Backend Hosting)
- **Student Program**: $50-200/mo free credits
  - Valid with .edu email or GitHub student pack
  - App Platform works great with Docker
  - Easy GitHub integration

### Vercel (Frontend Hosting)
- **Free tier**: 
  - Unlimited deployments
  - Custom domains
  - Edge functions
  - Perfect for React apps

---

## ⚙️ Architecture

```
┌─────────────────────────────────────┐
│        React Frontend (FREE)         │
│    Vercel or GitHub Pages hosting   │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│      FastAPI Backend (FREE)          │
│  Digital Ocean / Heroku / Railway   │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
  Grok    Pinecone   HuggingFace
  (LLM)   (Vector)  (Embeddings)
 FREE     FREE FREE  (local/free)
```

---

## 📊 Free Tier Limits

### HuggingFace (Local)
- ✅ Unlimited embeddings
- ✅ Runs offline
- ✅ No rate limits
- ⚠️ Slower than cloud APIs (but free!)

### Grok AI
- ⚠️ Limited requests/month (check xAI)
- ✅ Good enough for small projects
- ✅ Perfect for learning
- 💡 Upgrade only when needed

### Pinecone
- 📦 100K vectors max
- 1️⃣ 1 pod only
- ⏰ Projects expire after 7 days of inactivity
- 💡 Great for small government datasets

---

## 🎯 Use Cases (Within Free Limits)

✅ **Perfect for:**
- Learning RAG/LLM concepts
- Small government document datasets
- 100-5000 policy documents
- Student projects
- Prototyping

⚠️ **May hit limits for:**
- 100K+ documents
- High-traffic applications
- Production systems
- Real-time applications

---

## 💰 Cost Breakdown

| Item | Free | Paid (Not Needed) |
|------|------|------------------|
| Backend Server | DO Credits ($50-200) | $5-20/mo |
| Frontend Hosting | Vercel Free | - |
| Embeddings | HuggingFace (local) | OpenAI ($0.02/1K) |
| LLM | Grok Free Tier | GPT-4 ($30/mo+) |
| Vector DB | Pinecone Free (100K) | Pinecone Pro ($72+/mo) |
| **TOTAL** | **$0** | **$107+/mo** |

---

## 🚀 Deployment Options (All FREE)

### Option 1: Digital Ocean (Recommended for Students)
```bash
# Get $50-200 free credits via Student Program
# Requirements: .edu email or GitHub student pack

# Deploy with Docker (included)
docker-compose up
```

### Option 2: Railway.app
```bash
# Free tier: $5/mo credit
# Automatic GitHub deployments
# Great for small projects
```

### Option 3: Render.com
```bash
# Free tier available
# Easy GitHub integration
# Good documentation
```

### Option 4: Heroku (Via Student Pack)
```bash
# Included in GitHub Student Pack
# Easy deployment
# Good for learning
```

---

## 📚 Configuration for FREE Tier

All services are pre-configured in `.env.example`:

```env
# Grok AI (Free tier)
GROK_API_KEY=your_free_key

# Pinecone (100K vectors)
PINECONE_API_KEY=your_free_key
PINECONE_INDEX=starter-index  # Free tier index

# HuggingFace (Local, FREE)
EMBEDDINGS_MODEL=all-MiniLM-L6-v2  # 22MB, fast
EMBEDDINGS_PROVIDER=huggingface
```

---

## 🔒 Important Notes

### Free Tier Considerations
1. **Rate Limiting**: Grok AI has request limits
   - Use caching for common questions
   - Batch process documents
   
2. **Storage**: Pinecone has 100K vector limit
   - Remove old/unused documents
   - Compress document chunks
   
3. **Compute**: Backend on free DO credits
   - May have limited RAM/CPU
   - Use light models (all-MiniLM-L6-v2)

### Upgrading When Needed
- Start free, upgrade only when you hit limits
- Incremental costs as you grow
- Good for learning → small projects → production

---

## ❓ FAQ

**Q: Will my project go down after 7 days if inactive?**
A: Pinecone projects pause after 7 days. Just activate again when needed (free).

**Q: Can I use different embeddings models?**
A: Yes! All HuggingFace models work locally:
- Larger models = better quality but slower
- Smaller models = faster but less accurate

**Q: What if I exceed free limits?**
A: Services notify you before charging. You control upgrades completely.

**Q: Can I use this for production?**
A: Yes, but stay within limits. Great for:
- Small government datasets
- Learning systems
- Internal tools
- Startups on budget

---

## 🎓 Learning Resources

- **HuggingFace**: https://huggingface.co/docs
- **Grok AI**: https://docs.x.ai
- **Pinecone**: https://docs.pinecone.io
- **LangChain**: https://python.langchain.com
- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev

---

## 🤝 Support

Need help? Check:
1. Service documentation (links above)
2. Error logs in backend
3. GitHub issues in project repo
4. Service status pages for outages

---

## ✨ Next Steps

1. ✅ Get free API keys
2. ✅ Clone repository
3. ✅ Set up `.env` file
4. ✅ Run locally (`docker-compose up`)
5. ✅ Deploy to free hosting
6. ✅ Share your project!

**Welcome to free-tier AI! 🚀**
