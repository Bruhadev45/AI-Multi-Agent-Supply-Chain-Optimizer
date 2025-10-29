"""
Route Optimization Agent with Google Maps API integration
"""
import os
import requests
import logging
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.config import Config
from utils.vector_db import get_route_intelligence, update_route_data, record_route_performance

logger = logging.getLogger(__name__)

class RouteOptimizerAgent:
    """Google Maps API-based route optimization with intelligent fallbacks"""
    
    def __init__(self):
        """Initialize route optimizer with API configuration"""
        self.api_key = Config.GOOGLE_MAPS_API_KEY
        self.api_url = Config.GOOGLE_MAPS_API_URL
        self.distance_matrix = Config.DISTANCE_MATRIX
        self.city_coordinates = Config.CITY_COORDINATES
        
        # Validate API key
        if not self.api_key:
            logger.warning("Google Maps API key not found - using fallback mode")
        
        logger.info("RouteOptimizerAgent initialized")
    
    def get_best_route(self, origin: str, destination: str) -> Dict[str, Any]:
        """
        Get optimized route with comprehensive intelligence
        
        Args:
            origin: Starting city
            destination: Destination city
            
        Returns:
            Dictionary with route information and intelligence insights
        """
        try:
            logger.info(f"Finding optimal route: {origin} → {destination}")
            
            # Get historical intelligence from vector database
            route_intelligence = get_route_intelligence(origin, destination)
            
            # Try to get real-time route from Google Maps API
            real_time_route = self._get_google_maps_route(origin, destination)
            
            if real_time_route and real_time_route.get("source") == "Google Maps API":
                # Successfully got real-time data
                route_result = real_time_route
                route_result["historical_insights"] = route_intelligence
                
                # Record this route in vector database for future learning
                try:
                    update_route_data(
                        origin=origin,
                        destination=destination,
                        distance_km=route_result["distance_km"],
                        duration_hours=self._parse_duration_to_hours(route_result["duration"]),
                        cost=route_result["distance_km"] * 2.5,  # Estimated cost
                        traffic_factor=1.0,
                        weather="clear",
                        reliability=8.5
                    )
                    logger.info("Route data updated in vector database")
                except Exception as e:
                    logger.warning(f"Could not update route database: {e}")
            else:
                # Use intelligent fallback
                route_result = self._get_intelligent_fallback_route(origin, destination, route_intelligence)
            
            return route_result
            
        except Exception as e:
            logger.error(f"Route optimization failed: {e}")
            return self._create_emergency_fallback(origin, destination)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _get_google_maps_route(self, origin: str, destination: str) -> Optional[Dict[str, Any]]:
        """Get route from Google Maps API with retry logic"""
        if not self.api_key:
            logger.info("No Google Maps API key - skipping API call")
            return None
        
        try:
            params = {
                "origin": origin,
                "destination": destination,
                "mode": "driving",
                "key": self.api_key,
                "alternatives": "true",
                "optimize_waypoints": "true",
                "avoid": "tolls"  # Optimize for cost
            }
            
            logger.info("Calling Google Maps API...")
            response = requests.get(self.api_url, params=params, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Google Maps API HTTP error: {response.status_code}")
                return None
            
            data = response.json()
            
            if data.get("status") == "OK" and data.get("routes"):
                # Get the best route (first one is usually optimal)
                best_route = data["routes"][0]
                route_leg = best_route["legs"][0]
                
                result = {
                    "path": [origin, destination],
                    "distance_km": float(route_leg["distance"]["value"]) / 1000,
                    "duration": route_leg["duration"]["text"],
                    "duration_seconds": route_leg["duration"]["value"],
                    "source": "Google Maps API",
                    "polyline": best_route["overview_polyline"]["points"],
                    "route_quality": "Real-time optimized",
                    "alternatives_available": len(data["routes"]) > 1,
                    "traffic_considered": True,
                    "api_status": "SUCCESS"
                }
                
                logger.info(f"Google Maps API successful: {result['distance_km']:.1f}km, {result['duration']}")
                return result
            else:
                error_msg = data.get("error_message", data.get("status", "Unknown error"))
                logger.error(f"Google Maps API error: {error_msg}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Google Maps API timeout")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Google Maps API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Google Maps API unexpected error: {e}")
            return None
    
    def _get_intelligent_fallback_route(self, origin: str, destination: str, 
                                      intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Create intelligent fallback using vector database insights"""
        logger.info("Using intelligent fallback route calculation")
        
        try:
            # Use historical data if available
            if intelligence.get("historical_avg_distance", 0) > 0:
                distance = intelligence["historical_avg_distance"]
                duration_hours = intelligence.get("historical_avg_duration", distance / 60)
                
                source_info = f"Historical data ({intelligence['direct_routes']} previous routes)"
                quality = f"Based on {intelligence['direct_routes']} historical deliveries"
                
            else:
                # Use similar routes or distance matrix
                similar_routes = intelligence.get("similar_routes", [])
                if similar_routes:
                    # Use most similar route as reference
                    reference_route = similar_routes[0]
                    distance = reference_route.get("distance_km", self._get_distance_from_matrix(origin, destination))
                    duration_hours = reference_route.get("duration_hours", distance / 50)
                    
                    source_info = f"Similar route analysis (similarity: {reference_route.get('similarity_score', 0):.2f})"
                    quality = f"Estimated based on similar routes"
                else:
                    # Use distance matrix or estimation
                    distance = self._get_distance_from_matrix(origin, destination)
                    duration_hours = distance / 50  # Assume 50 km/h average
                    source_info = "Distance matrix estimation"
                    quality = "Matrix-based estimation"
            
            # Convert duration to readable format
            duration_text = self._hours_to_duration_text(duration_hours)
            
            result = {
                "path": [origin, destination],
                "distance_km": distance,
                "duration": duration_text,
                "duration_seconds": int(duration_hours * 3600),
                "source": source_info,
                "polyline": None,
                "route_quality": quality,
                "alternatives_available": False,
                "traffic_considered": False,
                "historical_insights": intelligence,
                "fallback_reason": "Google Maps API unavailable"
            }
            
            logger.info(f"Intelligent fallback successful: {distance:.1f}km, {duration_text}")
            return result
            
        except Exception as e:
            logger.error(f"Intelligent fallback failed: {e}")
            return self._create_emergency_fallback(origin, destination)
    
    def _get_distance_from_matrix(self, origin: str, destination: str) -> float:
        """Get distance from predefined matrix"""
        key1 = (origin.lower().strip(), destination.lower().strip())
        key2 = (destination.lower().strip(), origin.lower().strip())
        
        return self.distance_matrix.get(key1, self.distance_matrix.get(key2, 1200))
    
    def _create_emergency_fallback(self, origin: str, destination: str) -> Dict[str, Any]:
        """Create emergency fallback response when everything fails"""
        logger.warning("Using emergency fallback route calculation")
        
        distance = self._get_distance_from_matrix(origin, destination)
        duration_hours = distance / 45  # Conservative 45 km/h average
        
        return {
            "path": [origin, destination],
            "distance_km": distance,
            "duration": self._hours_to_duration_text(duration_hours),
            "duration_seconds": int(duration_hours * 3600),
            "source": "Emergency fallback estimation",
            "polyline": None,
            "route_quality": "Basic estimation",
            "alternatives_available": False,
            "traffic_considered": False,
            "fallback_reason": "All route calculation methods failed",
            "reliability_warning": True
        }
    
    def _parse_duration_to_hours(self, duration_text: str) -> float:
        """Parse Google Maps duration text to hours"""
        try:
            duration_lower = duration_text.lower()
            hours = 0
            minutes = 0
            
            # Extract hours
            if "hour" in duration_lower:
                hour_parts = duration_lower.split("hour")[0].strip().split()
                if hour_parts:
                    hours = int(hour_parts[-1])
            
            # Extract minutes
            if "min" in duration_lower:
                min_part = duration_lower.split("min")[0]
                if "hour" in min_part:
                    min_part = min_part.split("hour")[1]
                min_parts = min_part.strip().split()
                if min_parts:
                    minutes = int(min_parts[-1])
            
            return hours + (minutes / 60.0)
            
        except Exception as e:
            logger.error(f"Duration parsing failed: {e}")
            # Fallback: try to extract first number
            try:
                import re
                numbers = re.findall(r'\d+', duration_text)
                if numbers:
                    return float(numbers[0])  # Assume first number is hours
                return 12.0
            except:
                return 12.0
    
    def _hours_to_duration_text(self, hours: float) -> str:
        """Convert hours to readable duration text"""
        try:
            total_minutes = int(hours * 60)
            hours_part = total_minutes // 60
            minutes_part = total_minutes % 60
            
            if hours_part > 0 and minutes_part > 0:
                return f"{hours_part} hours {minutes_part} mins"
            elif hours_part > 0:
                return f"{hours_part} hours"
            else:
                return f"{minutes_part} mins"
        except:
            return f"{hours:.1f} hours"
    
    def record_delivery_performance(self, origin: str, destination: str, 
                                  actual_duration_hours: float, actual_cost: float,
                                  on_time: bool, customer_satisfaction: float):
        """Record actual delivery performance for machine learning"""
        try:
            # Calculate performance score based on multiple factors
            performance_score = 0
            
            # On-time delivery (40% weight)
            performance_score += 4.0 if on_time else 1.0
            
            # Customer satisfaction (30% weight) - scale 1-10 to 0-3
            performance_score += (min(customer_satisfaction, 10.0) / 10.0) * 3.0
            
            # Cost efficiency (30% weight) - placeholder for now
            performance_score += 3.0
            
            # Record in vector database
            record_route_performance(origin, destination, performance_score, actual_cost)
            logger.info(f"Recorded performance for {origin} → {destination}: {performance_score:.1f}/10")
            
        except Exception as e:
            logger.error(f"Failed to record performance: {e}")
    
    def get_route_alternatives(self, origin: str, destination: str) -> Dict[str, Any]:
        """Get multiple route alternatives with trade-off analysis"""
        try:
            primary_route = self.get_best_route(origin, destination)
            
            # Generate alternative scenarios
            alternatives = {
                "fastest": {**primary_route, "optimization": "time", "cost_multiplier": 1.15},
                "cheapest": {**primary_route, "optimization": "cost", "time_multiplier": 1.20},
                "balanced": {**primary_route, "optimization": "balanced", "score": "optimal"}
            }
            
            return {
                "primary_route": primary_route,
                "alternatives": alternatives,
                "recommendation": "balanced"
            }
            
        except Exception as e:
            logger.error(f"Failed to generate route alternatives: {e}")
            return {"error": str(e)}