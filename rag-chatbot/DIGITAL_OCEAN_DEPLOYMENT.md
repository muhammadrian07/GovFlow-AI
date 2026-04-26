# 🚀 Deploy to Digital Ocean (FREE with Student Credits)

Complete guide to deploy the free-tier RAG chatbot to Digital Ocean using App Platform.

---

## 💳 Digital Ocean Student Credits

### Get Free Credits
1. **GitHub Student Pack**: https://education.github.com/pack
   - $50 DO credit (free for students)
   - Sign up with .edu email

2. **Direct DO Student Program**: https://www.digitalocean.com/github-students
   - $200 credit (12 months)
   - Requires .edu email verification

### What You Get
- ✅ $50-200 free credits (expires after 12 months)
- ✅ Enough for backend + database + storage
- ✅ Full DO ecosystem access

---

## 📋 Prerequisites

- [x] GitHub account (with student verification)
- [x] Digital Ocean account
- [x] Applied for student credits
- [x] Project pushed to GitHub repo
- [x] All `.env` variables documented

---

## 🔧 Prepare Your Project

### 1. Add Procfile (for App Platform)
Create `backend/Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### 2. Add docker-compose.yml (Optional - for testing)
Already included in project ✅

### 3. Ensure requirements.txt is complete
```bash
# Check it includes all dependencies
cat backend/requirements.txt
```

### 4. Update CORS for Production
Edit `backend/app/core/config.py`:
```python
cors_origins: List[str] = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://yourdomain.com",  # Add after deployment
    "https://your-app.ondigitalocean.app"
]
```

---

## 🌐 Deploy Backend to App Platform

### Step 1: Create App on DO Console

1. Log into **DigitalOcean Dashboard**
   - https://cloud.digitalocean.com/apps

2. Click **"Create" → "App"**

3. **Choose Source**: GitHub
   - Authorize GitHub (one-time)
   - Select your repo
   - Select branch: `main`
   - Auto-detect: YES

### Step 2: Configure App Settings

**Service Detection**:
- ✅ Should auto-detect the backend
- If not, manually select:
  - Source dir: `backend/`
  - Build cmd: `pip install -r requirements.txt`
  - Run cmd: `uvicorn app.main:app --host 0.0.0.0 --port 8080`

**Component Settings**:
```
Name: govflow-api (or your choice)
Port: 8080
HTTP Routes: /
Auto-scale: 2-3 containers (within credits)
Instance Type: Basic ($5-12/mo, covered by credits)
```

### Step 3: Set Environment Variables

Click **"Env" tab** → **"Edit"** → Add these:

```env
# Required (FREE services)
GROK_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_INDEX=starter-index
PINECONE_ENVIRONMENT=us-east-1

# Embeddings (FREE, local)
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
EMBEDDINGS_PROVIDER=huggingface

# App Config
DEBUG=False
LOG_LEVEL=info
CORS_ORIGINS=["https://yourdomain.com"]
```

### Step 4: Deploy

1. Click **"Create Resources"**
2. Wait for deployment (5-10 minutes)
3. Get your URL: `https://govflow-api-xxxxx.ondigitalocean.app`

### Step 5: Test API

```bash
# Test health
curl https://govflow-api-xxxxx.ondigitalocean.app/health

# Check docs
https://govflow-api-xxxxx.ondigitalocean.app/docs
```

---

## 🎨 Deploy Frontend to Vercel (FREE)

### Step 1: Deploy on Vercel

1. Go to **Vercel Dashboard**: https://vercel.com

2. Click **"New Project"**

3. Import from GitHub
   - Select your repo
   - Select branch: `main`

4. **Configure**:
   - Build cmd: `npm run build` (in frontend/)
   - Output dir: `dist`
   - Root dir: `frontend/`

### Step 2: Add Environment Variables

Click **"Environment Variables"**:

```env
VITE_API_URL=https://govflow-api-xxxxx.ondigitalocean.app
```

### Step 3: Deploy

- Click **"Deploy"**
- Wait 2-5 minutes
- Get your URL: `https://govflow-ai.vercel.app`

---

## 🔗 Connect Frontend ↔ Backend

### After Both Deployments:

1. **Update Backend CORS**:
   ```python
   CORS_ORIGINS = [
       "https://govflow-ai.vercel.app",
       "https://yourdomain.com"
   ]
   ```

2. **Update Frontend API URL**:
   ```env
   VITE_API_URL=https://govflow-api-xxxxx.ondigitalocean.app
   ```

3. **Redeploy both**:
   - Push to GitHub (auto-redeploy on both)
   - Or manual redeploy in consoles

---

## 💾 Add Optional Database

### Free DO Options:

#### Option 1: PostgreSQL (within credits)
- Can add via DO console
- Use for storing user data, logs
- Free tier included in student credits

#### Option 2: Redis (Cache)
- For caching embedding results
- Free tier in student program

---

## 📊 Monitor Your Deployment

### In DO Console:

1. **Check Logs**:
   - App Platform → Your App → Logs
   - Debug deployment issues

2. **Check Metrics**:
   - CPU, Memory usage
   - Request count
   - Response times

3. **Check Resources**:
   - Container type and size
   - Current costs

---

## 💰 Cost Breakdown

### With $50-200 Student Credits:

| Service | Monthly Cost | Your Cost |
|---------|-------------|-----------|
| App Platform (2 containers) | $12-24 | FREE (credits) |
| Managed DB (optional) | $15-50 | FREE (credits) |
| Traffic/Bandwidth | $0.02/GB | Minimal |
| HuggingFace | $0 | $0 |
| Grok AI | Variable | FREE tier |
| Pinecone | $0 | FREE tier |
| **TOTAL** | $12-24 | **$0** ✅ |

**Credits last 12 months** - plenty of time to build!

---

## 🔐 Security Checklist

- [ ] Never commit `.env` files
- [ ] Use DO Secrets for sensitive keys
- [ ] Enable HTTPS (automatic on DO)
- [ ] Set up firewall rules (if needed)
- [ ] Monitor logs for errors
- [ ] Regular backups (if using DB)

---

## 🚨 Troubleshooting

### Deployment Failed
```bash
# Check logs in DO console
# Common issues:
# 1. Missing requirements.txt dependencies
# 2. Wrong Python version
# 3. API key invalid

# Fix:
# 1. Update requirements.txt locally
# 2. Push to GitHub
# 3. Trigger redeploy in DO console
```

### API Not Responding
```bash
# Check:
curl https://your-app.ondigitalocean.app/health

# If fails:
# 1. Check environment variables are set
# 2. Verify API keys are correct
# 3. Check app logs in DO console
```

### High CPU/Memory Usage
```bash
# Likely caused by:
# 1. Large embedding model (switch to all-MiniLM-L6-v2)
# 2. Too many concurrent requests
# 3. Memory leak in code

# Solution:
# 1. Increase container resources (costs more credits)
# 2. Enable auto-scaling
# 3. Add caching
```

---

## 🔄 CI/CD Pipeline (Auto-Deploy)

Digital Ocean automatically deploys when you push to GitHub:

1. Push to `main` branch
   ```bash
   git push origin main
   ```

2. GitHub notifies DO
3. DO rebuilds and deploys
4. New version live in 5-10 minutes

### Disable Auto-Deploy (if needed)
- App Platform → Settings → GitHub Auto-Deploy → Disable

---

## 📈 Scaling (When You Outgrow Free Tier)

If you hit limits (unlikely with credits):

1. **More Containers**: $5-12/mo per container
2. **Larger Containers**: $5-50/mo
3. **Database**: $15-500+/mo
4. **CDN**: $0.085/GB

But with free tier, you can learn & build first!

---

## 🎓 Next Steps

1. ✅ Get GitHub Student Pack
2. ✅ Add DO credits to account
3. ✅ Deploy backend to App Platform
4. ✅ Deploy frontend to Vercel
5. ✅ Connect them together
6. ✅ Share your project!

---

## 📚 Resources

- **DigitalOcean Docs**: https://docs.digitalocean.com
- **App Platform**: https://docs.digitalocean.com/products/app-platform
- **DO Community**: https://www.digitalocean.com/community
- **GitHub Student Pack**: https://education.github.com/pack

---

## ❓ FAQ

**Q: Do I need a credit card?**
A: No for GitHub Student Pack. Yes for direct DO account, but no charges with credits.

**Q: What happens after 12 months?**
A: Credits expire. You can pay as you go (~$5/mo) or shut down.

**Q: Can I use more than $200 credits?**
A: No, just $50-200 depending on your pack. But that's enough!

**Q: How do I monitor spending?**
A: DO Dashboard → Billing → Check usage in real-time.

**Q: Can I add a custom domain?**
A: Yes! Buy domain, add to App Platform settings (~$5-15/yr).

---

**Happy deploying! 🎉**
