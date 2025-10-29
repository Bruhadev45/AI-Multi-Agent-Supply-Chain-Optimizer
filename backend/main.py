"""
FastAPI Backend for AI Multi-Agent Supply Chain Optimizer
Replaces Streamlit with REST API endpoints
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import sys
import os

# Fix Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import Orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Supply Chain Optimizer API",
    description="Multi-Agent Supply Chain Optimization System",
    version="2.0.0"
)

# CORS Configuration - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development
        "http://localhost:3001",
        "http://localhost:7860",  # Hugging Face Spaces local
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:7860",
        "https://*.hf.space",  # Hugging Face Spaces production
        "*",  # Allow all origins for demo purposes
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator_instance: Optional[Orchestrator] = None

def get_orchestrator() -> Orchestrator:
    """Get or create orchestrator instance"""
    global orchestrator_instance
    if orchestrator_instance is None:
        try:
            logger.info("Initializing orchestrator...")
            orchestrator_instance = Orchestrator()
            logger.info("Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize system: {str(e)}")
    return orchestrator_instance


# ==================== Request/Response Models ====================

class AnalysisRequest(BaseModel):
    """Request model for supply chain analysis"""
    origin: str = Field(..., description="Origin city", example="Mumbai")
    destination: str = Field(..., description="Destination city", example="Delhi")
    scenario: str = Field(
        default="🟢 Normal Operations",
        description="Operational scenario",
        example="🟢 Normal Operations"
    )
    orders_csv: Optional[str] = Field(None, description="Path to orders CSV file")

class ScenarioConfig(BaseModel):
    """Scenario configuration response"""
    demand_multiplier: float
    cost_multiplier: float
    risk_level: str

class RouteInfo(BaseModel):
    """Route information response"""
    path: List[str]
    distance_km: float
    duration: str
    source: str
    polyline: Optional[str] = None
    route_quality: Optional[str] = None

class RiskInfo(BaseModel):
    """Risk assessment response"""
    condition: str
    temp: Optional[str] = None
    humidity: Optional[str] = None
    wind: Optional[str] = None
    risk_level: str
    source: str
    additional_risk: Optional[str] = None

class SystemHealth(BaseModel):
    """System health response"""
    overall_health: str
    success_rate: Optional[str] = None
    avg_response_time: Optional[str] = None
    api_status: Optional[Dict[str, bool]] = None

class AnalysisResponse(BaseModel):
    """Response model for supply chain analysis"""
    forecast: float
    forecast_original: float
    scenario_applied: str
    route_info: Dict[str, Any]
    best_vendor: str
    best_price: float
    original_price: float
    all_vendors: Optional[List[Dict[str, Any]]] = None
    risk: Dict[str, Any]
    crew_reasoning: str
    execution_metadata: Dict[str, Any]
    system_health: Dict[str, Any]
    recommendations_confidence: Dict[str, Any]

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    orchestrator_initialized: bool
    api_status: Optional[Dict[str, bool]] = None


# ==================== API Endpoints ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Multi-Agent Supply Chain Optimizer API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """Health check endpoint"""
    global orchestrator_instance

    api_status = None
    if orchestrator_instance:
        try:
            from utils.config import Config
            api_status = Config.validate_api_keys()
        except:
            pass

    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="2.0.0",
        orchestrator_initialized=orchestrator_instance is not None,
        api_status=api_status
    )

@app.post("/api/initialize", tags=["System"])
async def initialize_system():
    """Initialize the orchestrator system"""
    try:
        orchestrator = get_orchestrator()
        return {
            "status": "success",
            "message": "Orchestrator initialized successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def run_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Run comprehensive supply chain analysis

    This endpoint coordinates all AI agents to provide:
    - Demand forecasting
    - Route optimization
    - Cost analysis
    - Risk assessment
    - Strategic recommendations
    """
    try:
        logger.info(f"Starting analysis: {request.origin} → {request.destination}")

        # Get orchestrator
        orchestrator = get_orchestrator()

        # Run comprehensive analysis
        results = orchestrator.run_comprehensive_analysis(
            orders_csv=request.orders_csv,
            origin=request.origin,
            destination=request.destination,
            scenario=request.scenario
        )

        # Convert vendors DataFrame to list of dicts if present
        if 'all_vendors' in results and results['all_vendors'] is not None:
            try:
                if hasattr(results['all_vendors'], 'to_dict'):
                    results['all_vendors'] = results['all_vendors'].to_dict('records')
            except Exception as e:
                logger.warning(f"Failed to convert vendors: {e}")
                results['all_vendors'] = []

        logger.info(f"Analysis completed successfully")
        return results

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/scenarios", tags=["Configuration"])
async def get_scenarios():
    """Get available operational scenarios"""
    try:
        from utils.config import Config

        scenarios = [
            {
                "id": "normal",
                "name": "🟢 Normal Operations",
                "config": Config.get_scenario_config("🟢 Normal Operations")
            },
            {
                "id": "peak",
                "name": "📈 Peak Season Demand (+40%)",
                "config": Config.get_scenario_config("📈 Peak Season Demand (+40%)")
            },
            {
                "id": "fuel",
                "name": "💰 Fuel Price Surge (+25%)",
                "config": Config.get_scenario_config("💰 Fuel Price Surge (+25%)")
            },
            {
                "id": "monsoon",
                "name": "🌪️ Monsoon Disruption",
                "config": Config.get_scenario_config("🌪️ Monsoon Disruption")
            },
            {
                "id": "emergency",
                "name": "⚡ Emergency Supply",
                "config": Config.get_scenario_config("⚡ Emergency Supply")
            },
            {
                "id": "strike",
                "name": "🏭 Industrial Strike",
                "config": Config.get_scenario_config("🏭 Industrial Strike")
            }
        ]

        return {"scenarios": scenarios}

    except Exception as e:
        logger.error(f"Failed to fetch scenarios: {e}")
        # Return default scenarios as fallback
        return {
            "scenarios": [
                {
                    "id": "normal",
                    "name": "🟢 Normal Operations",
                    "config": {"demand_multiplier": 1.0, "cost_multiplier": 1.0, "risk_level": "Low"}
                }
            ]
        }

@app.get("/api/cities", tags=["Configuration"])
async def get_cities():
    """Get available cities for route planning"""
    cities = [
        {"name": "Mumbai", "coordinates": [19.0760, 72.8777]},
        {"name": "Delhi", "coordinates": [28.7041, 77.1025]},
        {"name": "Bangalore", "coordinates": [12.9716, 77.5946]},
        {"name": "Chennai", "coordinates": [13.0827, 80.2707]},
        {"name": "Kolkata", "coordinates": [22.5726, 88.3639]},
        {"name": "Hyderabad", "coordinates": [17.3850, 78.4867]},
        {"name": "Pune", "coordinates": [18.5204, 73.8567]},
        {"name": "Ahmedabad", "coordinates": [23.0225, 72.5714]},
        {"name": "Jaipur", "coordinates": [26.9124, 75.7873]},
        {"name": "Lucknow", "coordinates": [26.8467, 80.9462]},
        {"name": "Kanpur", "coordinates": [26.4499, 80.3319]},
        {"name": "Nagpur", "coordinates": [21.1458, 79.0882]},
        {"name": "Indore", "coordinates": [22.7196, 75.8577]},
        {"name": "Bhopal", "coordinates": [23.2599, 77.4126]}
    ]

    return {"cities": cities}

@app.get("/api/system/status", tags=["System"])
async def get_system_status():
    """Get detailed system status"""
    try:
        orchestrator = get_orchestrator()

        system_health = orchestrator._calculate_system_health()

        return {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "system_health": system_health,
            "execution_log": orchestrator.execution_log[-10:] if orchestrator.execution_log else [],
            "api_availability": orchestrator.api_availability
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.post("/api/system/reset", tags=["System"])
async def reset_system():
    """Reset the orchestrator system"""
    global orchestrator_instance

    try:
        logger.info("Resetting orchestrator...")
        orchestrator_instance = None
        orchestrator = get_orchestrator()

        return {
            "status": "success",
            "message": "System reset successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Reset failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Error Handlers ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "path": str(request.url),
        "docs": "/docs"
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal error: {exc}")
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "timestamp": datetime.now().isoformat()
    }


# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 50)
    logger.info("AI Supply Chain Optimizer API Starting...")
    logger.info("=" * 50)
    logger.info("Version: 2.0.0")
    logger.info("Framework: FastAPI")
    logger.info("Docs: http://localhost:8000/docs")
    logger.info("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("AI Supply Chain Optimizer API Shutting Down...")
    global orchestrator_instance
    orchestrator_instance = None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
