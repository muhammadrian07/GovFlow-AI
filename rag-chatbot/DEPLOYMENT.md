# 🌍 DEPLOYMENT GUIDE - RAG Chatbot

This guide covers deploying the RAG Chatbot to production.

## 📋 Pre-Deployment Checklist

- [ ] Backend environment variables configured
- [ ] Frontend API URL updated
- [ ] Database backups created
- [ ] Security review completed
- [ ] Rate limiting configured
- [ ] Monitoring set up
- [ ] Error logging enabled

## 🚀 Frontend Deployment (Vercel)

### 1. Prepare Frontend

```bash
cd frontend

# Build for production
npm run build

# Verify build
npm run preview
```

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 3. Deploy to Vercel

1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your project
4. Add environment variables:
   ```
   VITE_API_URL=https://your-backend.herokuapp.com/api
   ```
5. Deploy!

### 4. Custom Domain (Optional)

In Vercel dashboard:
1. Go to Settings > Domains
2. Add your custom domain
3. Update DNS records

## ⚙️ Backend Deployment (Render or Railway)

### Option A: Render

#### 1. Prepare Backend

```bash
cd backend

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > Procfile

# Add runtime.txt
echo "python-3.11.7" > runtime.txt
```

#### 2. Push to GitHub

```bash
git add .
git commit -m "Backend ready for deployment"
git push origin main
```

#### 3. Deploy on Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

5. Add Environment Variables:
   ```
   PINECONE_API_KEY=your_key
   OPENAI_API_KEY=your_key
   PINECONE_INDEX=govflow-index
   DEBUG=False
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```

6. Deploy!

### Option B: Railway

#### 1. Prepare Backend

Similar to Render, ensure requirements.txt is updated.

#### 2. Deploy on Railway

1. Go to https://railway.app
2. New Project > GitHub Repo
3. Configure:
   - Set NODE_ENV or PYTHON environment
   - Add environment variables

4. Add Environment Variables:
   ```
   PINECONE_API_KEY=your_key
   OPENAI_API_KEY=your_key
   PINECONE_INDEX=govflow-index
   DEBUG=False
   CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```

5. Deploy!

## 🔐 Security Hardening

### 1. Update Backend Config

In `backend/app/core/config.py`:

```python
# Before deployment, set:
DEBUG = False  # Disable debug mode

# Set appropriate CORS origins:
CORS_ORIGINS = ["https://your-domain.vercel.app"]

# Add authentication
JWT_SECRET_KEY = "your-secret-key-from-env"
```

### 2. Environment Variables

Never expose:
- API keys
- Database credentials
- Secret keys
- Debug info

Use environment variables for all secrets!

### 3. Rate Limiting

Add to `backend/app/main.py`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    # Limit to 10 requests per minute
    pass
```

### 4. Monitoring & Logging

Add Sentry for error tracking:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=0.1,
    environment="production"
)
```

## 📊 Production Checklist

### Backend

- [ ] DEBUG=False
- [ ] Error logging configured
- [ ] Rate limiting enabled
- [ ] CORS origins restricted
- [ ] Database optimized
- [ ] Health check endpoint working
- [ ] Graceful shutdown handling

### Frontend

- [ ] API URL points to production backend
- [ ] No console.log() statements
- [ ] Error boundaries implemented
- [ ] Loading states smooth
- [ ] Performance optimized

### Monitoring

- [ ] Error tracking set up
- [ ] Performance metrics tracked
- [ ] API usage monitored
- [ ] Alerts configured

## 🔄 Updating Production

### Deploy Frontend Update

```bash
cd frontend
npm run build
# Vercel auto-deploys when pushing to main
git push origin main
```

### Deploy Backend Update

```bash
cd backend
# Make changes...
git add .
git commit -m "Update feature"
git push origin main

# Render/Railway auto-deploys from Git
```

## 📈 Scaling

### If Backend Gets Slow

1. **Increase Render/Railway plan** - More resources
2. **Add caching** - Cache RAG results
3. **Optimize Pinecone** - Use larger vector dimensions strategically
4. **Use CDN** - Reduce latency

### If Costs Increase

1. **Set API quotas** - Limit token usage
2. **Implement caching** - Reduce API calls
3. **Batch requests** - Process multiple queries together
4. **Use cheaper models** - Consider gpt-3.5-turbo over gpt-4

## 🆘 Production Troubleshooting

### Backend Not Responding

1. Check Render/Railway logs
2. Verify environment variables set
3. Check API key quotas
4. Restart dyno/service

### High Latency

1. Check Pinecone response time
2. Monitor OpenAI API latency
3. Consider geographical distribution
4. Increase instance size

### API Errors

1. Check rate limits
2. Verify input validation
3. Review error logs
4. Check API quotas

## 📞 Support & Monitoring

### Render Dashboard

1. View real-time logs
2. Check CPU/Memory usage
3. See deployment history
4. Manage environment variables

### Railway Dashboard

Similar to Render:
1. Logs
2. Metrics
3. Deployments
4. Settings

## 🚨 Emergency Response

If production goes down:

1. **Check status** - Look at provider dashboard
2. **View logs** - Find error messages
3. **Rollback** - Revert to previous version
4. **Notify users** - Communicate status
5. **Fix** - Deploy patch
6. **Monitor** - Watch for recurrence

## 💰 Cost Optimization

### Monthly Cost Estimate

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Vercel | ✅ | $20/mo |
| Render | ✅ | $7/mo |
| Railway | ✅ | Pay as you go |
| Pinecone | ✅ (1 pod) | $1-100+/mo |
| OpenAI | - | $0.002-0.03/request |

### Save Money

1. Use free tier while testing
2. Implement caching (reduce API calls)
3. Use cheaper models (gpt-3.5-turbo)
4. Limit vector dimensions
5. Monitor usage closely

## 📝 Maintenance

### Weekly

- [ ] Check error logs
- [ ] Monitor API quotas
- [ ] Test critical flows

### Monthly

- [ ] Review performance metrics
- [ ] Update dependencies
- [ ] Backup important data
- [ ] Review costs

### Quarterly

- [ ] Security audit
- [ ] Performance optimization
- [ ] Update documentation
- [ ] Plan upgrades

---

**Deployment Complete!** 🎉
