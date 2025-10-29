"""
Configuration management for AI Supply Chain Optimizer
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    # File Paths
    DATA_DIR = "data"
    ORDERS_FILE = os.path.join(DATA_DIR, "orders.csv")
    VENDORS_FILE = os.path.join(DATA_DIR, "vendors.csv")
    
    # API Endpoints
    GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
    WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
    
    # Default Values
    DEFAULT_FORECAST_PERIODS = 7
    DEFAULT_ARIMA_ORDER = (2, 1, 2)
    DEFAULT_FUEL_EFFICIENCY = 15  # km/liter
    DEFAULT_CO2_EMISSION = 0.21  # kg per km
    
    # Scenario Multipliers
    SCENARIO_CONFIG = {
        "🟢 Normal Operations": {
            "demand_multiplier": 1.0,
            "cost_multiplier": 1.0,
            "risk_level": "Low"
        },
        "📈 Peak Season Demand (+40%)": {
            "demand_multiplier": 1.4,
            "cost_multiplier": 1.1,
            "risk_level": "Medium"
        },
        "💰 Fuel Price Surge (+25%)": {
            "demand_multiplier": 1.0,
            "cost_multiplier": 1.25,
            "risk_level": "Medium"
        },
        "🌪️ Monsoon Disruption": {
            "demand_multiplier": 0.9,
            "cost_multiplier": 1.15,
            "risk_level": "High"
        },
        "⚡ Emergency Supply": {
            "demand_multiplier": 1.2,
            "cost_multiplier": 1.3,
            "risk_level": "Medium"
        },
        "🏭 Industrial Strike": {
            "demand_multiplier": 1.0,
            "cost_multiplier": 1.2,
            "risk_level": "High"
        }
    }
    
    # City Coordinates for Mapping
    CITY_COORDINATES = {
        'mumbai': [19.0760, 72.8777],
        'delhi': [28.7041, 77.1025],
        'bangalore': [12.9716, 77.5946],
        'chennai': [13.0827, 80.2707],
        'kolkata': [22.5726, 88.3639],
        'hyderabad': [17.3850, 78.4867],
        'pune': [18.5204, 73.8567],
        'ahmedabad': [23.0225, 72.5714],
        'jaipur': [26.9124, 75.7873],
        'lucknow': [26.8467, 80.9462],
        'kanpur': [26.4499, 80.3319],
        'nagpur': [21.1458, 79.0882],
        'indore': [22.7196, 75.8577],
        'bhopal': [23.2599, 77.4126]
    }
    
    # Distance Matrix (km) for Indian Cities
    DISTANCE_MATRIX = {
        ("mumbai", "delhi"): 1400,
        ("mumbai", "bangalore"): 980,
        ("mumbai", "chennai"): 1340,
        ("mumbai", "kolkata"): 2000,
        ("mumbai", "hyderabad"): 710,
        ("mumbai", "pune"): 150,
        ("mumbai", "ahmedabad"): 530,
        ("delhi", "bangalore"): 2150,
        ("delhi", "chennai"): 2180,
        ("delhi", "kolkata"): 1500,
        ("delhi", "hyderabad"): 1580,
        ("delhi", "jaipur"): 280,
        ("delhi", "lucknow"): 550,
        ("bangalore", "chennai"): 350,
        ("bangalore", "hyderabad"): 570,
        ("bangalore", "kolkata"): 1880,
        ("chennai", "kolkata"): 1670,
        ("chennai", "hyderabad"): 630
    }
    
    @classmethod
    def get_scenario_config(cls, scenario: str) -> Dict[str, Any]:
        """Get configuration for a specific scenario"""
        return cls.SCENARIO_CONFIG.get(scenario, cls.SCENARIO_CONFIG["🟢 Normal Operations"])
    
    @classmethod
    def get_city_coordinates(cls, city: str) -> list:
        """Get coordinates for a city"""
        return cls.CITY_COORDINATES.get(city.lower().strip(), [23.5, 77.5])
    
    @classmethod
    def get_distance(cls, origin: str, destination: str) -> float:
        """Get distance between two cities"""
        key1 = (origin.lower().strip(), destination.lower().strip())
        key2 = (destination.lower().strip(), origin.lower().strip())
        
        return cls.DISTANCE_MATRIX.get(key1, cls.DISTANCE_MATRIX.get(key2, 1200))
    
    @classmethod
    def validate_api_keys(cls) -> Dict[str, bool]:
        """Validate API key availability"""
        return {
            "openai": bool(cls.OPENAI_API_KEY),
            "google_maps": bool(cls.GOOGLE_MAPS_API_KEY),
            "weather": bool(cls.WEATHER_API_KEY),
            "huggingface": bool(cls.HUGGINGFACE_API_KEY)
        }