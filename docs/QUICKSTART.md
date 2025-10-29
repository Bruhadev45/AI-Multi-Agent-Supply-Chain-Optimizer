# Quick Start Guide

## What Changed?

✅ **Removed**: Streamlit UI (replaced with FastAPI REST API)
✅ **Added**: FastAPI backend with REST endpoints
✅ **Added**: Next.js frontend API integration
✅ **Created**: Complete API client service
✅ **Updated**: All frontend components to fetch from API

## Start the Application (Easy Way)

### For macOS/Linux:

```bash
# Terminal 1 - Start Backend
./start-backend.sh

# Terminal 2 - Start Frontend
./start-frontend.sh
```

### For Windows:

```cmd
REM Terminal 1 - Start Backend
start-backend.bat

REM Terminal 2 - Start Frontend
start-frontend.bat
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## First Time Setup

### 1. Backend API Keys

Create `backend/.env` file with your API keys:

```bash
OPENAI_API_KEY=sk-...
GOOGLE_MAPS_API_KEY=...
WEATHER_API_KEY=...
HUGGINGFACE_API_KEY=...  # Optional
```

### 2. Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## How to Use

1. **Open Frontend**: http://localhost:3000
2. **Go to Scenario Builder**: Click "Scenario" in the sidebar
3. **Configure Your Analysis**:
   - Step 1: Choose scenario (Normal, Peak Season, etc.)
   - Step 2: Select origin and destination cities
   - Step 3: Set constraints (optional)
   - Step 4: Review and click "Run Optimization"
4. **View Results**: Automatically redirected to Dashboard with results

## Key Features

### Backend API Endpoints
- `POST /api/analyze` - Run supply chain analysis
- `GET /api/scenarios` - Get available scenarios
- `GET /api/cities` - Get city list
- `GET /health` - Check API health

### Frontend Pages
- **Dashboard**: View analysis results and metrics
- **Scenario Builder**: Configure and run analysis
- **Agent Details**: View AI agent performance
- **Vendor Routes**: Visualize routes and vendors
- **Reports**: Comprehensive analysis reports
- **Settings**: System configuration

## Troubleshooting

### Backend Won't Start

**Error**: Port 8000 already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Error**: API keys not working
- Check `.env` file exists in `backend/` directory
- Verify API keys are valid
- Restart backend after adding keys

### Frontend Can't Connect

**Error**: "API Connection Failed"
- Ensure backend is running on port 8000
- Check `frontend/.env.local` has correct URL
- Verify backend shows "Application startup complete" in logs

### Dependencies Issues

**Backend:**
```bash
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Testing the API

You can test the API directly using the interactive docs:

1. Go to http://localhost:8000/docs
2. Try the `/health` endpoint first
3. Try `/api/cities` to see available cities
4. Try `/api/analyze` with sample data:
   ```json
   {
     "origin": "Mumbai",
     "destination": "Delhi",
     "scenario": "🟢 Normal Operations"
   }
   ```

## What Was Removed

The old Streamlit application (`app.py`) has been backed up to `app.py.streamlit.backup`. The new FastAPI backend (`main.py`) provides the same functionality through REST API endpoints.

**Key differences:**
- Old: Streamlit web UI at http://localhost:8501
- New: FastAPI REST API at http://localhost:8000
- Frontend: Now uses Next.js at http://localhost:3000

## Next Steps

1. ✅ Start both servers
2. ✅ Test the connection
3. ✅ Run your first analysis
4. Consider adding authentication (see README.md)
5. Consider deploying to production

## Need Help?

- Check full README.md for detailed documentation
- View API docs at http://localhost:8000/docs
- Check system status at http://localhost:8000/api/system/status
