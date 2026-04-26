# Quick Start Guide

## 🚀 One-Command Setup

### macOS / Linux
```bash
chmod +x start.sh
./start.sh
```

### Windows
```bash
start.bat
```

## 📋 What It Does

1. ✅ Checks Python and Node.js installation
2. ✅ Creates Python virtual environment
3. ✅ Installs backend dependencies
4. ✅ Installs frontend dependencies
5. ✅ Creates `.env` files from examples
6. ✅ Provides instructions to start servers

## 🎯 After Setup

Follow the on-screen instructions to start both servers:

**Backend (Terminal 1):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

**Visit:** http://localhost:5173

## 🐳 Docker Setup (Alternative)

```bash
# Create .env file with your keys
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Start with Docker Compose
docker-compose up

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## ⚡ Troubleshooting

### Python not found
```bash
# Install Python from python.org
# Or use package manager:
# macOS: brew install python3
# Ubuntu: sudo apt install python3
```

### Node not found
```bash
# Install Node from nodejs.org
# Or use package manager:
# macOS: brew install node
# Ubuntu: sudo apt install nodejs npm
```

### Permission denied (start.sh)
```bash
chmod +x start.sh
```

### Port already in use
```bash
# Backend uses 8000
# Frontend uses 5173
# If ports are busy, edit in config files
```

---

Need help? See SETUP.md for detailed instructions.
