#!/bin/bash

# RAG Chatbot - Quick Start Script
# This script sets up and runs the entire application

set -e  # Exit on error

echo "🚀 RAG Chatbot - Quick Start"
echo "================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites found${NC}"

# Setup Backend
echo -e "${BLUE}Setting up backend...${NC}"

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env with your API keys${NC}"
    echo "   - PINECONE_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - PINECONE_INDEX"
    read -p "Press Enter to continue..."
fi

echo -e "${GREEN}✅ Backend setup complete${NC}"

cd ..

# Setup Frontend
echo -e "${BLUE}Setting up frontend...${NC}"

cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install -q

# Create .env.local if not exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
fi

echo -e "${GREEN}✅ Frontend setup complete${NC}"

cd ..

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "To start the application, run in separate terminals:"
echo ""
echo -e "${YELLOW}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate  # (or venv\\Scripts\\activate on Windows)"
echo "  python -m uvicorn app.main:app --reload"
echo ""
echo -e "${YELLOW}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:5173"
echo ""
