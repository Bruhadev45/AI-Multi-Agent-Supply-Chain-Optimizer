"""
Risk Monitoring Agent for weather and operational risk assessment
"""
import requests
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from utils.config import Config

logger = logging.getLogger(__name__)

class RiskMonitorAgent:
    """Comprehensive risk assessment with weather and operational factors"""
    
    def __init__(self):
        """Initialize risk monitor with API configuration"""
        self.weather_key = Config.WEATHER_API_KEY
        self.weather_url = Config.WEATHER_API_URL
        
        # Risk thresholds and categories
        self.weather_risk_categories = {
            'high_risk': ['storm', 'thunder', 'cyclone', 'snow', 'blizzard', 'tornado', 'hurricane'],
            'medium_risk': ['rain', 'drizzle', 'fog', 'mist', 'cloudy'],
            'low_risk': ['clear', 'sunny', 'partly cloudy', 'overcast']
        }
        
        self.seasonal_factors = {
            'monsoon_months': [6, 7, 8, 9],  # June to September
            'winter_months': [12, 1, 2],      # December to February
            'summer_months': [3, 4, 5]        # March to May
        }
        
        logger.info("RiskMonitorAgent initialized")
        if not self.weather_key:
            logger.warning("Weather API key not found - using fallback risk assessment")
    
    def check_weather(self, location: str) -> Dict[str, Any]:
        """
        Comprehensive weather risk assessment
        
        Args:
            location: City or location name
            
        Returns:
            Dictionary with weather data and risk assessment
        """
        try:
            logger.info(f"Checking weather risk for: {location}")
            
            # Try to get real weather data
            weather_data = self._get_weather_api_data(location)
            
            if weather_data and not weather_data.get('error'):
                # Process real weather data
                risk_assessment = self._analyze_weather_risk(weather_data)
                risk_assessment.update(weather_data)
                risk_assessment['data_source'] = 'Weather API'
                
                logger.info(f"Weather API successful: {risk_assessment['risk_level']}")
                return risk_assessment
            else:
                # Use intelligent fallback
                logger.info("Using intelligent weather fallback")
                return self._get_intelligent_weather_fallback(location, weather_data)
                
        except Exception as e:
            logger.error(f"Weather risk assessment failed: {e}")
            return self._get_emergency_fallback(location)
    
    def _get_weather_api_data(self, location: str) -> Optional[Dict[str, Any]]:
        """Get weather data from API"""
        if not self.weather_key:
            return None
        
        try:
            params = {
                "key": self.weather_key,
                "q": location,
                "aqi": "no"
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Weather API HTTP error: {response.status_code}")
                return {"error": f"HTTP {response.status_code}"}
            
            data = response.json()
            
            if "current" in data:
                current = data["current"]
                condition = current["condition"]["text"].lower()
                
                return {
                    "condition": current["condition"]["text"],
                    "temp": f"{current['temp_c']}°C",
                    "humidity": f"{current['humidity']}%",
                    "wind": f"{current['wind_kph']} km/h",
                    "wind_speed_raw": current['wind_kph'],
                    "visibility": f"{current.get('vis_km', 10)} km",
                    "pressure": f"{current.get('pressure_mb', 1013)} mb",
                    "condition_raw": condition,
                    "temp_raw": current['temp_c'],
                    "humidity_raw": current['humidity']
                }
            elif "error" in data:
                return {"error": f"WeatherAPI error: {data['error']['message']}"}
            else:
                return {"error": "No weather data available"}
                
        except requests.exceptions.Timeout:
            return {"error": "Weather API timeout"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Weather API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Weather API unexpected error: {str(e)}"}
    
    def _analyze_weather_risk(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather conditions and calculate risk"""
        try:
            condition = weather_data.get('condition_raw', '').lower()
            wind_speed = weather_data.get('wind_speed_raw', 0)
            temp = weather_data.get('temp_raw', 25)
            humidity = weather_data.get('humidity_raw', 50)
            
            risk_score = 0
            risk_factors = []
            
            # Weather condition risk
            if any(risk_word in condition for risk_word in self.weather_risk_categories['high_risk']):
                risk_score += 30
                risk_factors.append("Severe weather conditions")
            elif any(risk_word in condition for risk_word in self.weather_risk_categories['medium_risk']):
                risk_score += 15
                risk_factors.append("Moderate weather impact")
            
            # Wind speed risk
            if wind_speed > 40:
                risk_score += 20
                risk_factors.append("High wind speeds")
            elif wind_speed > 25:
                risk_score += 10
                risk_factors.append("Moderate winds")
            
            # Temperature extremes
            if temp < 0 or temp > 45:
                risk_score += 15
                risk_factors.append("Extreme temperatures")
            elif temp < 5 or temp > 40:
                risk_score += 8
                risk_factors.append("Temperature concerns")
            
            # Humidity impact
            if humidity > 85:
                risk_score += 5
                risk_factors.append("High humidity")
            
            # Seasonal risk adjustment
            current_month = datetime.now().month
            if current_month in self.seasonal_factors['monsoon_months']:
                risk_score += 10
                risk_factors.append("Monsoon season")
            elif current_month in self.seasonal_factors['winter_months']:
                risk_score += 5
                risk_factors.append("Winter conditions")
            
            # Determine risk level
            if risk_score >= 50:
                risk_level = "🔴 High"
                impact_description = "High risk of delays and operational challenges"
            elif risk_score >= 25:
                risk_level = "🟡 Medium"
                impact_description = "Moderate risk, monitor conditions closely"
            else:
                risk_level = "🟢 Low"
                impact_description = "Minimal weather-related risks"
            
            return {
                'risk_level': risk_level,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'impact_description': impact_description,
                'recommendations': self._get_risk_recommendations(risk_score, risk_factors)
            }
            
        except Exception as e:
            logger.error(f"Weather risk analysis failed: {e}")
            return {
                'risk_level': '🟡 Medium',
                'risk_score': 25,
                'risk_factors': ['Analysis error'],
                'impact_description': 'Unable to assess weather risk',
                'recommendations': ['Monitor conditions manually']
            }
    
    def _get_intelligent_weather_fallback(self, location: str, error_data: Optional[Dict]) -> Dict[str, Any]:
        """Intelligent fallback based on location and seasonal patterns"""
        try:
            current_month = datetime.now().month
            current_hour = datetime.now().hour
            
            # Seasonal risk assessment
            base_risk = 0
            risk_factors = []
            
            if current_month in self.seasonal_factors['monsoon_months']:
                base_risk += 20
                risk_factors.append("Monsoon season - higher rain probability")
                condition = "Partly Cloudy (Monsoon Season)"
                temp = "28°C"
                humidity = "75%"
            elif current_month in self.seasonal_factors['winter_months']:
                base_risk += 10
                risk_factors.append("Winter season - fog/visibility issues")
                condition = "Clear (Winter)"
                temp = "18°C"
                humidity = "60%"
            else:
                base_risk += 5
                risk_factors.append("Summer season - heat considerations")
                condition = "Clear"
                temp = "32°C"
                humidity = "45%"
            
            # Location-specific adjustments
            location_lower = location.lower()
            if any(coastal in location_lower for coastal in ['mumbai', 'chennai', 'kolkata']):
                base_risk += 5
                risk_factors.append("Coastal location - weather variability")
                humidity = "70%"
            
            if 'delhi' in location_lower and current_month in [11, 12, 1]:
                base_risk += 10
                risk_factors.append("Delhi winter - fog and pollution")
            
            # Time of day considerations
            if 5 <= current_hour <= 7:
                base_risk += 5
                risk_factors.append("Early morning - potential fog/mist")
            
            # Determine fallback risk level
            if base_risk >= 30:
                risk_level = "🟡 Medium"
                impact = "Seasonal risk factors present"
            elif base_risk >= 15:
                risk_level = "🟡 Medium"
                impact = "Some weather considerations"
            else:
                risk_level = "🟢 Low"
                impact = "Minimal expected weather impact"
            
            result = {
                'condition': condition,
                'temp': temp,
                'humidity': humidity,
                'wind': "15 km/h",
                'risk_level': risk_level,
                'risk_score': base_risk,
                'risk_factors': risk_factors,
                'impact_description': impact,
                'data_source': 'Intelligent Seasonal Estimation',
                'recommendations': self._get_risk_recommendations(base_risk, risk_factors)
            }
            
            # Add API error info if available
            if error_data and error_data.get('error'):
                result['api_error'] = error_data['error']
            
            return result
            
        except Exception as e:
            logger.error(f"Intelligent fallback failed: {e}")
            return self._get_emergency_fallback(location)
    
    def _get_emergency_fallback(self, location: str) -> Dict[str, Any]:
        """Emergency fallback when all methods fail"""
        return {
            'condition': 'Unknown',
            'temp': '25°C',
            'humidity': '60%',
            'wind': '10 km/h',
            'risk_level': '🟡 Medium',
            'risk_score': 25,
            'risk_factors': ['Weather data unavailable'],
            'impact_description': 'Unable to assess weather conditions',
            'data_source': 'Emergency Fallback',
            'recommendations': [
                'Monitor local weather manually',
                'Prepare for potential delays',
                'Have contingency plans ready'
            ],
            'warning': 'Weather assessment unavailable - use manual monitoring'
        }
    
    def _get_risk_recommendations(self, risk_score: int, risk_factors: List[str]) -> List[str]:
        """Generate specific recommendations based on risk assessment"""
        recommendations = []
        
        try:
            if risk_score >= 50:
                recommendations.extend([
                    "Consider postponing delivery if possible",
                    "Use covered/protected transport vehicles",
                    "Increase insurance coverage for this delivery",
                    "Plan for significant delays and extra costs",
                    "Have backup routes and vendors ready"
                ])
            elif risk_score >= 25:
                recommendations.extend([
                    "Monitor weather conditions closely",
                    "Inform customer of potential delays",
                    "Use experienced drivers familiar with conditions",
                    "Ensure vehicle is properly equipped",
                    "Have contingency communication plan"
                ])
            else:
                recommendations.extend([
                    "Proceed with standard precautions",
                    "Monitor conditions during transit",
                    "Maintain normal delivery schedule"
                ])
            
            # Specific factor-based recommendations
            if any('wind' in factor.lower() for factor in risk_factors):
                recommendations.append("Secure cargo properly for high winds")
            
            if any('rain' in factor.lower() or 'monsoon' in factor.lower() for factor in risk_factors):
                recommendations.append("Use waterproof packaging and covers")
            
            if any('fog' in factor.lower() or 'visibility' in factor.lower() for factor in risk_factors):
                recommendations.append("Allow extra time for reduced visibility conditions")
            
            if any('temperature' in factor.lower() for factor in risk_factors):
                recommendations.append("Consider temperature-sensitive cargo protection")
            
            return recommendations[:5]  # Limit to top 5 recommendations
            
        except Exception as e:
            logger.error(f"Risk recommendations failed: {e}")
            return ["Monitor conditions and use standard safety precautions"]
    
    def get_extended_forecast(self, location: str, days: int = 3) -> Dict[str, Any]:
        """Get extended weather forecast for route planning"""
        try:
            # This would typically call a forecast API
            # For now, provide a basic forecast structure
            
            forecast_days = []
            current_date = datetime.now()
            
            for i in range(days):
                forecast_date = current_date + timedelta(days=i)
                
                # Basic forecast estimation
                day_forecast = {
                    'date': forecast_date.strftime('%Y-%m-%d'),
                    'day_name': forecast_date.strftime('%A'),
                    'condition': 'Partly Cloudy',
                    'temp_high': 30,
                    'temp_low': 22,
                    'rain_probability': 20,
                    'wind_speed': 15,
                    'risk_level': '🟢 Low'
                }
                
                # Adjust for current conditions if we have them
                current_weather = self.check_weather(location)
                if not current_weather.get('error') and i == 0:
                    day_forecast.update({
                        'condition': current_weather.get('condition', 'Unknown'),
                        'risk_level': current_weather.get('risk_level', '🟡 Medium')
                    })
                
                forecast_days.append(day_forecast)
            
            return {
                'location': location,
                'forecast_days': forecast_days,
                'overall_risk': self._assess_forecast_risk(forecast_days),
                'planning_recommendations': self._get_forecast_recommendations(forecast_days)
            }
            
        except Exception as e:
            logger.error(f"Extended forecast failed: {e}")
            return {
                'location': location,
                'error': str(e),
                'fallback_advice': 'Check local weather services for multi-day forecast'
            }
    
    def _assess_forecast_risk(self, forecast_days: List[Dict]) -> str:
        """Assess overall risk from forecast"""
        try:
            risk_levels = [day.get('risk_level', '🟡 Medium') for day in forecast_days]
            
            if any('🔴' in level for level in risk_levels):
                return '🔴 High'
            elif any('🟡' in level for level in risk_levels):
                return '🟡 Medium'
            else:
                return '🟢 Low'
                
        except:
            return '🟡 Medium'
    
    def _get_forecast_recommendations(self, forecast_days: List[Dict]) -> List[str]:
        """Generate recommendations based on forecast"""
        recommendations = []
        
        try:
            high_rain_days = sum(1 for day in forecast_days if day.get('rain_probability', 0) > 60)
            high_wind_days = sum(1 for day in forecast_days if day.get('wind_speed', 0) > 25)
            
            if high_rain_days > 1:
                recommendations.append("Multiple days of rain expected - plan for delays")
            
            if high_wind_days > 0:
                recommendations.append("High winds forecast - secure cargo properly")
            
            if len(recommendations) == 0:
                recommendations.append("Weather conditions appear favorable for delivery")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Forecast recommendations failed: {e}")
            return ["Monitor weather conditions during delivery period"]