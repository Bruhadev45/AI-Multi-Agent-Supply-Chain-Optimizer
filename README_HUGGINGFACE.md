---
title: AI Multi-Agent Supply Chain Optimizer
emoji: 🚚
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# 🚚 AI Multi-Agent Supply Chain Optimizer

A sophisticated multi-agent AI system for supply chain optimization using Next.js frontend and FastAPI backend with AI-powered decision making.

## Features

- **AI-Powered Demand Forecasting**: Predict demand using advanced time series analysis
- **Intelligent Route Optimization**: Find optimal routes with real-time traffic and weather data
- **Multi-Agent Coordination**: Specialized AI agents for different aspects of supply chain
- **Real-time Risk Assessment**: Monitor and assess risks across the supply chain
- **Cost Optimization**: Compare vendors and optimize procurement decisions
- **Interactive Dashboard**: Modern, responsive UI with dark mode support

## Tech Stack

- **Frontend**: Next.js 16, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.10
- **AI Framework**: Multi-agent orchestration system
- **APIs**: OpenRouter, OpenWeather, OpenRouteService

## Usage

Once deployed, you can:

1. Select origin and destination cities
2. Choose an operational scenario (Normal, Peak Season, Emergency, etc.)
3. Run comprehensive analysis
4. View AI-powered recommendations
5. Export results for further analysis

## Configuration

The following environment variables should be set in Hugging Face Spaces:

### Backend Environment Variables

```bash
# Required: OpenRouter API for AI agents
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional: For enhanced functionality
OPENWEATHER_API_KEY=your_openweather_api_key
OPENROUTESERVICE_API_KEY=your_openrouteservice_api_key
```

### How to Set Environment Variables in Hugging Face Spaces

1. Go to your Space settings
2. Navigate to "Variables and secrets"
3. Add the above environment variables as "Secrets"

## Architecture

```
┌─────────────────┐
│   Next.js UI    │  (Port 7860)
│   Frontend      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │  (Port 8000)
│  Backend        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Agents      │
│  - Demand       │
│  - Route        │
│  - Cost         │
│  - Risk         │
│  - Strategy     │
└─────────────────┘
```

## Development

To run locally:

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## License

MIT License - See LICENSE file for details

## Credits

Built with Claude Code and deployed on Hugging Face Spaces
