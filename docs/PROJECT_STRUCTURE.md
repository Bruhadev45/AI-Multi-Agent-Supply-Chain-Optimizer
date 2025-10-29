# 📁 Project Structure

## Directory Overview

```
AI-Multi-Agent-Supply-Chain-Optimizer/
├── README.md                      # Main project documentation
├── .gitignore                     # Git ignore rules
├── start-backend.sh/.bat         # Quick start scripts
├── start-frontend.sh/.bat        # Quick start scripts
│
├── docs/                         # 📚 Documentation
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── QUICKSTART.md             # Quick start guide
│   ├── NEW_FEATURES_ADDED.md     # Latest features
│   ├── PRODUCTION_READY_GUIDE.md # Production checklist
│   └── LOGISTICS_FEATURES.md     # Feature roadmap
│
├── backend/                      # 🐍 Python Backend (FastAPI)
│   ├── main.py                   # API server entry point
│   ├── orchestrator.py           # Multi-agent orchestration
│   ├── crew_setup.py             # CrewAI configuration
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   ├── agents/                   # AI agent definitions
│   │   ├── __init__.py
│   │   ├── demand_agent.py
│   │   ├── route_agent.py
│   │   ├── cost_agent.py
│   │   ├── risk_agent.py
│   │   └── coordinator.py
│   ├── data/                     # Data files
│   │   ├── cities.json
│   │   └── scenarios.json
│   ├── utils/                    # Utility functions
│   └── venv/                     # Virtual environment
│
└── frontend/                     # ⚛️ React Frontend (Next.js 16)
    ├── package.json              # npm dependencies
    ├── next.config.mjs           # Next.js configuration
    ├── tsconfig.json             # TypeScript configuration
    ├── postcss.config.mjs        # PostCSS configuration
    ├── .env.example              # Environment variables template
    ├── .env.local                # Local environment variables
    │
    ├── app/                      # Next.js App Router
    │   ├── layout.tsx            # Root layout (Poppins font)
    │   ├── page.tsx              # Main page
    │   └── globals.css           # Global styles
    │
    ├── components/               # React Components
    │   ├── chat/                 # AI Chatbot
    │   │   └── ai-chatbot.tsx
    │   ├── layout/               # Layout components
    │   │   ├── main-layout.tsx
    │   │   ├── sidebar.tsx
    │   │   └── top-nav.tsx       # With dark mode toggle
    │   ├── map/                  # Map components
    │   │   └── route-map.tsx
    │   ├── pages/                # Page components
    │   │   ├── main-optimizer.tsx
    │   │   ├── shipment-tracking.tsx  # With search/filter
    │   │   ├── vendor-routes.tsx
    │   │   ├── enhanced-agent-details.tsx
    │   │   ├── progressive-agents.tsx
    │   │   └── strategic-recommendations.tsx
    │   └── ui/                   # UI components (Radix + Shadcn)
    │       ├── button.tsx
    │       ├── card.tsx
    │       ├── badge.tsx
    │       ├── input.tsx
    │       ├── theme-toggle.tsx  # Dark mode toggle
    │       ├── export-button.tsx # Export functionality
    │       └── ... (30+ components)
    │
    ├── lib/                      # Utilities
    │   ├── api-client.ts         # API client with TypeScript types
    │   └── utils.ts              # Helper functions
    │
    ├── hooks/                    # React Hooks
    │   └── use-toast.ts
    │
    ├── public/                   # Static assets
    │   ├── next.svg
    │   └── vercel.svg
    │
    └── node_modules/             # Dependencies (gitignored)
```

---

## 🎯 Key Files Explained

### Backend

**main.py**
- FastAPI server setup
- CORS configuration
- API routes
- Health check endpoint

**orchestrator.py**
- Multi-agent coordination
- Analysis pipeline
- Response formatting

**agents/**
- 5 specialized AI agents
- Each handles specific domain
- Collaborative decision-making

---

### Frontend

**app/layout.tsx**
- Root layout with Poppins font
- Theme provider
- Analytics setup

**app/page.tsx**
- Main application logic
- State management
- API integration

**components/pages/**
- Main application pages
- Business logic components

**components/ui/**
- Reusable UI components
- Consistent design system

---

## 🗂️ File Naming Conventions

### Components
- PascalCase for component files: `MainOptimizer.tsx`
- kebab-case for utility files: `api-client.ts`

### Directories
- lowercase for folders: `components/`, `utils/`
- Descriptive names: `pages/`, `layout/`

---

## 📦 Build Artifacts (Gitignored)

```
frontend/.next/          # Next.js build output
frontend/node_modules/   # npm packages
backend/venv/            # Python virtual environment
backend/__pycache__/     # Python cache
*.log                    # Log files
.DS_Store               # macOS files
```

---

## 🔒 Environment Files

**backend/.env**
```
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

**frontend/.env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Dependencies

### Backend (Python 3.9+)
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv
- (Optional) CrewAI

### Frontend (Node 18+)
- Next.js 16
- React 18
- TypeScript
- Tailwind CSS
- Radix UI
- React Leaflet
- Recharts

---

## 🚀 Quick Commands

**Start Development**:
```bash
# Backend
./start-backend.sh

# Frontend
./start-frontend.sh
```

**Build Production**:
```bash
# Frontend
cd frontend && npm run build

# Backend
cd backend && pip install -r requirements.txt
```

---

## 📝 Notes

- All component files use "use client" directive
- TypeScript strict mode enabled
- ESLint and Prettier configured
- Dark mode fully implemented
- Mobile-responsive design

---

Last Updated: October 29, 2025
