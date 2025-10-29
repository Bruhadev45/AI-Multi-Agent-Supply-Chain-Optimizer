"""
Vector Database for Route Intelligence and Historical Learning
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np

# Simple in-memory vector database for route intelligence
# In production, you could replace this with ChromaDB or similar

logger = logging.getLogger(__name__)

class RouteVectorDB:
    """Simple vector database for route intelligence"""
    
    def __init__(self):
        self.routes = []  # List of route records
        self.performance_history = []  # Performance tracking
        
        # Initialize with some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample route data"""
        sample_routes = [
            {
                'origin': 'mumbai',
                'destination': 'delhi',
                'distance_km': 1400,
                'duration_hours': 18.5,
                'cost': 3500,
                'weather': 'clear',
                'traffic_factor': 1.1,
                'reliability': 8.5,
                'timestamp': '2024-01-15T10:00:00'
            },
            {
                'origin': 'bangalore',
                'destination': 'chennai',
                'distance_km': 350,
                'duration_hours': 6.2,
                'cost': 875,
                'weather': 'partly_cloudy',
                'traffic_factor': 1.0,
                'reliability': 9.1,
                'timestamp': '2024-01-20T14:30:00'
            }
        ]
        
        for route in sample_routes:
            self.routes.append(route)
    
    def add_route(self, origin: str, destination: str, distance_km: float, 
                  duration_hours: float, cost: float, weather: str = "clear",
                  traffic_factor: float = 1.0, reliability: float = 8.0):
        """Add a new route record"""
        route_record = {
            'origin': origin.lower().strip(),
            'destination': destination.lower().strip(),
            'distance_km': distance_km,
            'duration_hours': duration_hours,
            'cost': cost,
            'weather': weather,
            'traffic_factor': traffic_factor,
            'reliability': reliability,
            'timestamp': datetime.now().isoformat()
        }
        
        self.routes.append(route_record)
        logger.info(f"Added route: {origin} → {destination}")
    
    def get_route_history(self, origin: str, destination: str) -> List[Dict]:
        """Get historical data for a specific route"""
        origin_clean = origin.lower().strip()
        dest_clean = destination.lower().strip()
        
        matching_routes = []
        for route in self.routes:
            if (route['origin'] == origin_clean and route['destination'] == dest_clean) or \
               (route['origin'] == dest_clean and route['destination'] == origin_clean):
                matching_routes.append(route)
        
        return matching_routes
    
    def get_similar_routes(self, origin: str, destination: str, limit: int = 5) -> List[Dict]:
        """Find similar routes based on cities and distance"""
        origin_clean = origin.lower().strip()
        dest_clean = destination.lower().strip()
        
        similar_routes = []
        
        for route in self.routes:
            similarity_score = 0
            
            # Same origin or destination adds similarity
            if route['origin'] == origin_clean or route['destination'] == origin_clean:
                similarity_score += 0.5
            if route['origin'] == dest_clean or route['destination'] == dest_clean:
                similarity_score += 0.5
            
            # Add distance-based similarity (closer distances are more similar)
            if similarity_score > 0:
                route['similarity_score'] = similarity_score
                similar_routes.append(route)
        
        # Sort by similarity and return top results
        similar_routes.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
        return similar_routes[:limit]
    
    def record_performance(self, origin: str, destination: str, 
                          performance_score: float, actual_cost: float):
        """Record delivery performance for learning"""
        performance_record = {
            'origin': origin.lower().strip(),
            'destination': destination.lower().strip(),
            'performance_score': performance_score,
            'actual_cost': actual_cost,
            'timestamp': datetime.now().isoformat()
        }
        
        self.performance_history.append(performance_record)
        logger.info(f"Recorded performance: {origin} → {destination} = {performance_score:.1f}")
    
    def get_route_intelligence(self, origin: str, destination: str) -> Dict[str, Any]:
        """Get comprehensive route intelligence"""
        # Get direct route history
        direct_routes = self.get_route_history(origin, destination)
        
        # Get similar routes
        similar_routes = self.get_similar_routes(origin, destination)
        
        # Calculate averages for direct routes
        intelligence = {
            'direct_routes': len(direct_routes),
            'similar_routes': similar_routes,
            'has_historical_data': len(direct_routes) > 0
        }
        
        if direct_routes:
            intelligence.update({
                'historical_avg_distance': np.mean([r['distance_km'] for r in direct_routes]),
                'historical_avg_duration': np.mean([r['duration_hours'] for r in direct_routes]),
                'historical_avg_cost': np.mean([r['cost'] for r in direct_routes]),
                'avg_reliability': np.mean([r['reliability'] for r in direct_routes]),
                'weather_patterns': [r['weather'] for r in direct_routes]
            })
        
        return intelligence


# Global instance
_route_db = RouteVectorDB()

# Public interface functions
def update_route_data(origin: str, destination: str, distance_km: float, 
                     duration_hours: float, cost: float, traffic_factor: float = 1.0,
                     weather: str = "clear", reliability: float = 8.0):
    """Add route data to vector database"""
    global _route_db
    _route_db.add_route(origin, destination, distance_km, duration_hours, 
                       cost, weather, traffic_factor, reliability)

def get_route_intelligence(origin: str, destination: str) -> Dict[str, Any]:
    """Get route intelligence from vector database"""
    global _route_db
    return _route_db.get_route_intelligence(origin, destination)

def record_route_performance(origin: str, destination: str, 
                           performance_score: float, actual_cost: float):
    """Record route performance for machine learning"""
    global _route_db
    _route_db.record_performance(origin, destination, performance_score, actual_cost)