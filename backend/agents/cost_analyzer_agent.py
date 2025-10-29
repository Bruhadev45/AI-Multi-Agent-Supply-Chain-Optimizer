"""
Cost Analysis Agent for vendor comparison and optimization
"""
import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any, Optional
from utils.config import Config

logger = logging.getLogger(__name__)

class CostAnalyzerAgent:
    """Advanced cost analysis with sustainability and reliability metrics"""
    
    def __init__(self, vendor_file: Optional[str] = None):
        """
        Initialize cost analyzer with vendor data
        
        Args:
            vendor_file: Path to vendor CSV file
        """
        self.vendor_file = vendor_file or Config.VENDORS_FILE
        self.vendors = self._load_or_create_vendor_data()
        
        logger.info(f"CostAnalyzerAgent initialized with {len(self.vendors)} vendors")
    
    def _load_or_create_vendor_data(self) -> pd.DataFrame:
        """Load vendor data or create sample data"""
        try:
            # Try to load existing vendor file
            if self.vendor_file and pd.io.common.file_exists(self.vendor_file):
                vendors = pd.read_csv(self.vendor_file)
                logger.info(f"Loaded vendor data from {self.vendor_file}")
                return self._validate_vendor_data(vendors)
            else:
                # Create sample vendor data
                logger.info("Creating sample vendor data")
                return self._create_sample_vendor_data()
                
        except Exception as e:
            logger.error(f"Failed to load vendor data: {e}")
            return self._create_sample_vendor_data()
    
    def _create_sample_vendor_data(self) -> pd.DataFrame:
        """Create comprehensive sample vendor database"""
        vendors_data = {
            'vendor': [
                'LogiTech Express', 'GreenShip Co', 'FastTrack Logistics', 
                'EcoFreight Solutions', 'SpeedyDelivery', 'CargoMaster',
                'BlueOcean Shipping', 'RailLink Express'
            ],
            'cost_per_km': [2.5, 3.2, 2.8, 3.5, 2.3, 2.9, 2.7, 2.1],
            'emission_per_km': [0.8, 0.3, 0.6, 0.2, 0.9, 0.7, 0.4, 0.15],
            'reliability_score': [8.5, 9.2, 7.8, 9.5, 7.2, 8.1, 8.8, 9.0],
            'delivery_speed': [
                'Standard', 'Eco', 'Fast', 'Eco+', 'Express', 
                'Standard', 'Eco', 'Rail'
            ],
            'service_quality': [8.0, 9.0, 7.5, 9.2, 6.8, 8.3, 8.7, 8.9],
            'max_capacity_kg': [5000, 3000, 8000, 4000, 6000, 7000, 4500, 10000],
            'insurance_coverage': [1000000, 800000, 1200000, 900000, 600000, 1100000, 1000000, 1500000]
        }
        
        return pd.DataFrame(vendors_data)
    
    def _validate_vendor_data(self, vendors: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean vendor data"""
        required_columns = ['vendor', 'cost_per_km', 'emission_per_km', 'reliability_score']
        
        # Check for required columns
        for col in required_columns:
            if col not in vendors.columns:
                logger.warning(f"Missing required column: {col}")
                return self._create_sample_vendor_data()
        
        # Clean data
        vendors = vendors.copy()
        
        # Ensure numeric columns are numeric
        numeric_columns = ['cost_per_km', 'emission_per_km', 'reliability_score']
        for col in numeric_columns:
            vendors[col] = pd.to_numeric(vendors[col], errors='coerce')
        
        # Remove rows with missing critical data
        vendors = vendors.dropna(subset=required_columns)
        
        # Add missing optional columns with defaults
        if 'delivery_speed' not in vendors.columns:
            vendors['delivery_speed'] = 'Standard'
        
        if 'service_quality' not in vendors.columns:
            vendors['service_quality'] = 8.0
            
        if 'max_capacity_kg' not in vendors.columns:
            vendors['max_capacity_kg'] = 5000
        
        return vendors
    
    def compare_vendors(self, distance_km: float, weight_kg: float = 1000, 
                       priority: str = "balanced") -> Tuple[str, float, pd.DataFrame]:
        """
        Compare vendors with comprehensive analysis
        
        Args:
            distance_km: Route distance in kilometers
            weight_kg: Cargo weight in kilograms
            priority: Optimization priority ('cost', 'speed', 'eco', 'balanced')
            
        Returns:
            Tuple of (best_vendor, best_price, all_vendors_analysis)
        """
        try:
            if distance_km <= 0:
                logger.error("Invalid distance provided")
                distance_km = 1000  # Default fallback
            
            # Create analysis dataframe
            analysis = self.vendors.copy()
            
            # Calculate costs and metrics
            analysis['total_cost'] = analysis['cost_per_km'] * distance_km
            analysis['co2_emission'] = analysis['emission_per_km'] * distance_km
            analysis['weight_feasible'] = analysis['max_capacity_kg'] >= weight_kg
            
            # Calculate efficiency scores
            analysis['cost_efficiency'] = self._calculate_cost_efficiency(analysis['total_cost'])
            analysis['eco_efficiency'] = self._calculate_eco_efficiency(analysis['co2_emission'])
            analysis['service_score'] = (analysis['reliability_score'] + analysis['service_quality']) / 2
            
            # Apply weight constraint
            feasible_vendors = analysis[analysis['weight_feasible']].copy()
            
            if feasible_vendors.empty:
                logger.warning(f"No vendors can handle {weight_kg}kg cargo")
                # Use all vendors but add surcharge for overweight
                feasible_vendors = analysis.copy()
                feasible_vendors['total_cost'] *= 1.25  # 25% surcharge
                feasible_vendors['overweight_surcharge'] = True
            else:
                feasible_vendors['overweight_surcharge'] = False
            
            # Calculate composite scores based on priority
            feasible_vendors['composite_score'] = self._calculate_composite_score(
                feasible_vendors, priority
            )
            
            # Find best vendor
            best_idx = feasible_vendors['composite_score'].idxmax()
            best_vendor = feasible_vendors.loc[best_idx, 'vendor']
            best_price = feasible_vendors.loc[best_idx, 'total_cost']
            
            # Add ranking
            feasible_vendors['rank'] = feasible_vendors['composite_score'].rank(ascending=False)
            feasible_vendors = feasible_vendors.sort_values('rank')
            
            logger.info(f"Best vendor selected: {best_vendor} at ₹{best_price:,.2f}")
            
            return best_vendor, best_price, feasible_vendors
            
        except Exception as e:
            logger.error(f"Vendor comparison failed: {e}")
            return self._get_fallback_vendor(distance_km)
    
    def _calculate_cost_efficiency(self, costs: pd.Series) -> pd.Series:
        """Calculate cost efficiency scores (0-10 scale)"""
        try:
            min_cost = costs.min()
            max_cost = costs.max()
            
            if max_cost == min_cost:
                return pd.Series([10.0] * len(costs), index=costs.index)
            
            # Invert so lower cost = higher efficiency
            normalized = (max_cost - costs) / (max_cost - min_cost)
            return normalized * 10
            
        except Exception as e:
            logger.error(f"Cost efficiency calculation failed: {e}")
            return pd.Series([7.0] * len(costs), index=costs.index)
    
    def _calculate_eco_efficiency(self, emissions: pd.Series) -> pd.Series:
        """Calculate environmental efficiency scores (0-10 scale)"""
        try:
            min_emission = emissions.min()
            max_emission = emissions.max()
            
            if max_emission == min_emission:
                return pd.Series([10.0] * len(emissions), index=emissions.index)
            
            # Invert so lower emission = higher efficiency
            normalized = (max_emission - emissions) / (max_emission - min_emission)
            return normalized * 10
            
        except Exception as e:
            logger.error(f"Eco efficiency calculation failed: {e}")
            return pd.Series([7.0] * len(emissions), index=emissions.index)
    
    def _calculate_composite_score(self, vendors: pd.DataFrame, priority: str) -> pd.Series:
        """Calculate composite scores based on optimization priority"""
        try:
            # Define weighting schemes
            weights = {
                'cost': {'cost': 0.6, 'service': 0.2, 'eco': 0.1, 'reliability': 0.1},
                'speed': {'service': 0.4, 'reliability': 0.3, 'cost': 0.2, 'eco': 0.1},
                'eco': {'eco': 0.5, 'service': 0.2, 'reliability': 0.2, 'cost': 0.1},
                'balanced': {'cost': 0.3, 'service': 0.25, 'eco': 0.25, 'reliability': 0.2}
            }
            
            weight_set = weights.get(priority, weights['balanced'])
            
            # Normalize reliability score to 0-10 scale
            reliability_normalized = vendors['reliability_score']
            service_normalized = vendors['service_score']
            
            # Calculate weighted composite score
            composite = (
                weight_set['cost'] * vendors['cost_efficiency'] +
                weight_set['service'] * service_normalized +
                weight_set['eco'] * vendors['eco_efficiency'] +
                weight_set['reliability'] * reliability_normalized
            )
            
            return composite
            
        except Exception as e:
            logger.error(f"Composite score calculation failed: {e}")
            return pd.Series([7.0] * len(vendors), index=vendors.index)
    
    def _get_fallback_vendor(self, distance_km: float) -> Tuple[str, float, pd.DataFrame]:
        """Provide fallback vendor when analysis fails"""
        logger.warning("Using fallback vendor selection")
        
        fallback_vendor = "Emergency Logistics"
        fallback_cost = distance_km * 3.5  # Premium rate
        
        fallback_df = pd.DataFrame({
            'vendor': [fallback_vendor],
            'total_cost': [fallback_cost],
            'cost_per_km': [3.5],
            'emission_per_km': [0.8],
            'reliability_score': [6.0],
            'delivery_speed': ['Standard'],
            'service_quality': [6.0],
            'composite_score': [6.0],
            'rank': [1],
            'fallback_mode': [True]
        })
        
        return fallback_vendor, fallback_cost, fallback_df
    
    def get_sustainability_report(self, distance_km: float) -> Dict[str, Any]:
        """Generate comprehensive sustainability analysis"""
        try:
            analysis = self.vendors.copy()
            analysis['total_cost'] = analysis['cost_per_km'] * distance_km
            analysis['co2_emission'] = analysis['emission_per_km'] * distance_km
            
            # Calculate sustainability metrics
            total_emissions = analysis['co2_emission'].sum()
            avg_emission = analysis['co2_emission'].mean()
            best_eco_vendor = analysis.loc[analysis['co2_emission'].idxmin(), 'vendor']
            worst_eco_vendor = analysis.loc[analysis['co2_emission'].idxmax(), 'vendor']
            
            # Carbon footprint categories
            low_carbon = analysis[analysis['emission_per_km'] < 0.4]
            medium_carbon = analysis[(analysis['emission_per_km'] >= 0.4) & (analysis['emission_per_km'] < 0.7)]
            high_carbon = analysis[analysis['emission_per_km'] >= 0.7]
            
            return {
                'total_route_distance': distance_km,
                'average_co2_emission': avg_emission,
                'best_eco_vendor': best_eco_vendor,
                'worst_eco_vendor': worst_eco_vendor,
                'low_carbon_options': len(low_carbon),
                'medium_carbon_options': len(medium_carbon),
                'high_carbon_options': len(high_carbon),
                'carbon_savings_potential': analysis['co2_emission'].max() - analysis['co2_emission'].min(),
                'eco_recommendations': self._get_eco_recommendations(analysis)
            }
            
        except Exception as e:
            logger.error(f"Sustainability report failed: {e}")
            return {'error': str(e)}
    
    def _get_eco_recommendations(self, analysis: pd.DataFrame) -> list:
        """Generate environmental recommendations"""
        recommendations = []
        
        try:
            best_eco = analysis.loc[analysis['co2_emission'].idxmin()]
            avg_emission = analysis['co2_emission'].mean()
            
            if best_eco['co2_emission'] < avg_emission * 0.7:
                recommendations.append(f"Choose {best_eco['vendor']} for 30%+ emission reduction")
            
            eco_vendors = analysis[analysis['emission_per_km'] < 0.4]
            if len(eco_vendors) > 1:
                recommendations.append(f"{len(eco_vendors)} low-carbon vendors available")
            
            if len(recommendations) == 0:
                recommendations.append("Consider rail or consolidated shipping for better eco-efficiency")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Eco recommendations failed: {e}")
            return ["Sustainability analysis unavailable"]