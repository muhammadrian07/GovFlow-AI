@echo off
REM RAG Chatbot - Quick Start Script for Windows

echo.
echo 🚀 RAG Chatbot - Quick Start
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+
    pause
    exit /b 1
)
echo ✅ Python found

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)
echo ✅ Node.js found

REM Setup Backend
echo.
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit backend\.env with your API keys
    echo    - PINECONE_API_KEY
    echo    - OPENAI_API_KEY
    echo    - PINECONE_INDEX
    pause
)

echo ✅ Backend setup complete
cd ..

REM Setup Frontend
echo.
echo Setting up frontend...
cd frontend

echo Installing Node dependencies...
call npm install -q

if not exist ".env.local" (
    echo Creating .env.local file...
    copy .env.example .env.local
)

echo ✅ Frontend setup complete
cd ..

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the application, run in separate terminals:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python -m uvicorn app.main:app --reload
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then visit: http://localhost:5173
echo.
pause
