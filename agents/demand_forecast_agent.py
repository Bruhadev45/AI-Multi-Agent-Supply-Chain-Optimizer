"""
Demand Forecasting Agent using ARIMA modeling with comprehensive fallback methods
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import logging
import warnings
from typing import Union, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

# Suppress statsmodels warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

logger = logging.getLogger(__name__)

class DemandForecastAgent:
    """
    Advanced demand forecasting agent with multiple modeling approaches
    
    Features:
    - ARIMA time series modeling
    - Exponential smoothing fallback
    - Seasonal decomposition analysis
    - Moving average methods
    - Confidence scoring and validation
    - Scenario-based adjustments
    """
    
    def __init__(self, arima_order: tuple = (2, 1, 2)):
        """
        Initialize demand forecast agent
        
        Args:
            arima_order: ARIMA model parameters (p, d, q)
        """
        self.arima_order = arima_order
        self.model = None
        self.last_forecast = None
        self.forecast_history = []
        self.model_performance = {
            'arima': {'success_count': 0, 'total_attempts': 0},
            'exponential': {'success_count': 0, 'total_attempts': 0},
            'moving_average': {'success_count': 0, 'total_attempts': 0}
        }
        
        logger.info(f"DemandForecastAgent initialized with ARIMA order: {self.arima_order}")
    
    def forecast(self, orders_df: pd.DataFrame, periods: int = 1, 
                confidence_level: float = 0.95) -> float:
        """
        Generate demand forecast using hierarchical modeling approach
        
        Args:
            orders_df: DataFrame with 'orders' column and optional 'date' column
            periods: Number of periods to forecast ahead
            confidence_level: Confidence level for prediction intervals
            
        Returns:
            Forecasted demand value
        """
        try:
            start_time = datetime.now()
            logger.info(f"Starting demand forecast for {periods} periods ahead")
            
            # Step 1: Validate and prepare data
            orders_data, data_quality = self._prepare_and_validate_data(orders_df)
            
            if data_quality['is_valid'] == False:
                logger.warning(f"Data quality issues: {data_quality['issues']}")
                return self._get_fallback_forecast()
            
            # Step 2: Try hierarchical forecasting methods
            forecast_result = self._hierarchical_forecast(orders_data, periods, confidence_level)
            
            # Step 3: Validate and store results
            if forecast_result['success']:
                forecast_value = max(0, round(forecast_result['forecast'], 2))
                
                # Store forecast history for learning
                self._store_forecast_result(forecast_value, forecast_result['method'], 
                                          forecast_result['confidence'])
                
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"Forecast completed: {forecast_value} ({forecast_result['method']}) "
                          f"in {execution_time:.2f}s")
                
                return forecast_value
            else:
                logger.warning("All forecasting methods failed, using fallback")
                return self._get_fallback_forecast()
                
        except Exception as e:
            logger.error(f"Forecast generation failed: {e}")
            return self._get_fallback_forecast()
    
    def _prepare_and_validate_data(self, orders_df: pd.DataFrame) -> Tuple[pd.Series, Dict]:
        """
        Comprehensive data preparation and validation
        
        Returns:
            Tuple of (cleaned_data, quality_report)
        """
        quality_report = {'is_valid': True, 'issues': [], 'data_points': 0, 'missing_values': 0}
        
        try:
            # Check if DataFrame is valid
            if orders_df is None or orders_df.empty:
                quality_report['is_valid'] = False
                quality_report['issues'].append("Empty or None DataFrame")
                return pd.Series(), quality_report
            
            # Check for orders column
            if 'orders' not in orders_df.columns:
                quality_report['is_valid'] = False
                quality_report['issues'].append("Missing 'orders' column")
                return pd.Series(), quality_report
            
            # Extract and clean orders data
            orders_data = orders_df['orders'].copy()
            original_length = len(orders_data)
            
            # Convert to numeric, handling errors
            orders_data = pd.to_numeric(orders_data, errors='coerce')
            
            # Count missing values before cleanup
            missing_before = orders_data.isna().sum()
            quality_report['missing_values'] = missing_before
            
            # Remove NaN values
            orders_data = orders_data.dropna()
            
            # Remove negative values
            negative_count = (orders_data < 0).sum()
            if negative_count > 0:
                quality_report['issues'].append(f"{negative_count} negative values removed")
                orders_data = orders_data[orders_data >= 0]
            
            # Handle zeros (replace with small positive value)
            zero_count = (orders_data == 0).sum()
            if zero_count > 0:
                quality_report['issues'].append(f"{zero_count} zero values adjusted")
                orders_data = orders_data.replace(0, 1)
            
            # Check final data quality
            final_length = len(orders_data)
            quality_report['data_points'] = final_length
            
            if final_length < 5:
                quality_report['is_valid'] = False
                quality_report['issues'].append(f"Insufficient data points: {final_length} < 5")
            elif final_length < original_length * 0.7:
                quality_report['issues'].append(f"Significant data loss: {final_length}/{original_length}")
            
            # Statistical validation
            if final_length >= 5:
                std_dev = orders_data.std()
                mean_val = orders_data.mean()
                cv = std_dev / mean_val if mean_val > 0 else float('inf')
                
                if cv > 2.0:  # Very high variability
                    quality_report['issues'].append(f"High variability detected (CV: {cv:.2f})")
                
                # Check for outliers using IQR method
                Q1 = orders_data.quantile(0.25)
                Q3 = orders_data.quantile(0.75)
                IQR = Q3 - Q1
                outlier_count = ((orders_data < (Q1 - 1.5 * IQR)) | 
                               (orders_data > (Q3 + 1.5 * IQR))).sum()
                
                if outlier_count > final_length * 0.1:  # More than 10% outliers
                    quality_report['issues'].append(f"Many outliers detected: {outlier_count}")
            
            return orders_data, quality_report
            
        except Exception as e:
            logger.error(f"Data preparation failed: {e}")
            quality_report['is_valid'] = False
            quality_report['issues'].append(f"Data preparation error: {str(e)}")
            return pd.Series(), quality_report
    
    def _hierarchical_forecast(self, orders_data: pd.Series, periods: int, 
                             confidence_level: float) -> Dict[str, Any]:
        """
        Try multiple forecasting methods in order of sophistication
        """
        methods = [
            ('arima', self._arima_forecast),
            ('exponential_smoothing', self._exponential_smoothing_forecast),
            ('seasonal_decompose', self._seasonal_decompose_forecast),
            ('moving_average', self._moving_average_forecast),
            ('trend_forecast', self._trend_forecast)
        ]
        
        for method_name, method_func in methods:
            try:
                self.model_performance[method_name]['total_attempts'] += 1
                
                result = method_func(orders_data, periods, confidence_level)
                
                if result is not None and not np.isnan(result['forecast']):
                    self.model_performance[method_name]['success_count'] += 1
                    result['method'] = method_name
                    result['success'] = True
                    
                    logger.info(f"Forecast successful using {method_name}: {result['forecast']:.2f}")
                    return result
                    
            except Exception as e:
                logger.warning(f"{method_name} forecast failed: {e}")
                continue
        
        # If all methods fail
        return {'success': False, 'forecast': None, 'method': 'none', 'confidence': 0.0}
    
    def _arima_forecast(self, orders_data: pd.Series, periods: int, 
                       confidence_level: float) -> Dict[str, Any]:
        """
        ARIMA forecasting with automatic parameter optimization
        """
        try:
            if len(orders_data) < 10:
                raise ValueError("Insufficient data for ARIMA model")
            
            # Try primary ARIMA order
            try:
                model = ARIMA(orders_data, order=self.arima_order)
                model_fit = model.fit()
                self.model = model_fit
                
                # Generate forecast with confidence intervals
                forecast_result = model_fit.forecast(steps=periods, alpha=1-confidence_level)
                forecast_value = forecast_result.iloc[-1] if hasattr(forecast_result, 'iloc') else float(forecast_result)
                
                # Calculate confidence from model
                confidence = self._calculate_arima_confidence(model_fit, orders_data)
                
                return {
                    'forecast': forecast_value,
                    'confidence': confidence,
                    'model_info': {
                        'aic': model_fit.aic,
                        'bic': model_fit.bic,
                        'order': self.arima_order
                    }
                }
                
            except:
                # Try alternative ARIMA orders
                alternative_orders = [(1, 1, 1), (1, 0, 1), (2, 0, 1), (1, 1, 0)]
                
                for order in alternative_orders:
                    try:
                        model = ARIMA(orders_data, order=order)
                        model_fit = model.fit()
                        forecast_result = model_fit.forecast(steps=periods)
                        forecast_value = forecast_result.iloc[-1] if hasattr(forecast_result, 'iloc') else float(forecast_result)
                        
                        confidence = self._calculate_arima_confidence(model_fit, orders_data)
                        
                        logger.info(f"ARIMA forecast successful with order {order}")
                        return {
                            'forecast': forecast_value,
                            'confidence': confidence,
                            'model_info': {'aic': model_fit.aic, 'order': order}
                        }
                    except:
                        continue
                
                raise ValueError("All ARIMA orders failed")
                
        except Exception as e:
            logger.error(f"ARIMA forecasting failed: {e}")
            return None
    
    def _exponential_smoothing_forecast(self, orders_data: pd.Series, periods: int, 
                                      confidence_level: float) -> Dict[str, Any]:
        """
        Exponential smoothing with trend and seasonal components
        """
        try:
            # Determine seasonal period
            seasonal_period = min(12, len(orders_data) // 3) if len(orders_data) >= 24 else None
            
            # Try different exponential smoothing configurations
            configs = [
                {'trend': 'add', 'seasonal': 'add', 'seasonal_periods': seasonal_period},
                {'trend': 'add', 'seasonal': None},
                {'trend': None, 'seasonal': None}
            ]
            
            for config in configs:
                try:
                    if config['seasonal_periods'] is None:
                        config.pop('seasonal_periods', None)
                        config['seasonal'] = None
                    
                    model = ExponentialSmoothing(orders_data, **config)
                    model_fit = model.fit()
                    
                    forecast_result = model_fit.forecast(periods)
                    forecast_value = forecast_result.iloc[-1] if hasattr(forecast_result, 'iloc') else float(forecast_result)
                    
                    # Calculate confidence based on residuals
                    residuals = model_fit.resid
                    residual_std = residuals.std()
                    confidence = max(0.3, 1 - (residual_std / orders_data.mean()))
                    
                    return {
                        'forecast': forecast_value,
                        'confidence': confidence,
                        'model_info': {
                            'trend': config.get('trend'),
                            'seasonal': config.get('seasonal'),
                            'aic': getattr(model_fit, 'aic', None)
                        }
                    }
                    
                except Exception as e:
                    logger.debug(f"Exponential smoothing config failed: {config}, error: {e}")
                    continue
            
            raise ValueError("All exponential smoothing configurations failed")
            
        except Exception as e:
            logger.error(f"Exponential smoothing failed: {e}")
            return None
    
    def _seasonal_decompose_forecast(self, orders_data: pd.Series, periods: int, 
                                   confidence_level: float) -> Dict[str, Any]:
        """
        Seasonal decomposition-based forecasting
        """
        try:
            if len(orders_data) < 14:  # Need at least 2 weeks for seasonal decomposition
                raise ValueError("Insufficient data for seasonal decomposition")
            
            # Determine seasonal period
            seasonal_period = min(7, len(orders_data) // 2)
            
            # Perform seasonal decomposition
            decomposition = seasonal_decompose(orders_data, model='additive', 
                                             period=seasonal_period, extrapolate_trend='freq')
            
            # Extract components
            trend = decomposition.trend.dropna()
            seasonal = decomposition.seasonal
            
            # Forecast trend using linear regression
            if len(trend) >= 3:
                x = np.arange(len(trend))
                trend_coef = np.polyfit(x, trend, 1)
                future_trend = np.polyval(trend_coef, len(trend) + periods - 1)
            else:
                future_trend = trend.iloc[-1] if len(trend) > 0 else orders_data.mean()
            
            # Get seasonal component for forecast period
            seasonal_component = seasonal.iloc[(len(orders_data) + periods - 1) % seasonal_period]
            
            # Combine trend and seasonal
            forecast_value = future_trend + seasonal_component
            
            # Calculate confidence
            residuals = decomposition.resid.dropna()
            residual_std = residuals.std()
            confidence = max(0.4, 1 - (residual_std / orders_data.mean()))
            
            return {
                'forecast': forecast_value,
                'confidence': confidence,
                'model_info': {
                    'seasonal_period': seasonal_period,
                    'trend_slope': trend_coef[0] if len(trend) >= 3 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Seasonal decomposition failed: {e}")
            return None
    
    def _moving_average_forecast(self, orders_data: pd.Series, periods: int, 
                               confidence_level: float) -> Dict[str, Any]:
        """
        Advanced moving average forecasting with trend adjustment
        """
        try:
            data_length = len(orders_data)
            
            # Determine optimal window size
            if data_length >= 21:
                window_size = 7  # Weekly average
            elif data_length >= 10:
                window_size = min(5, data_length // 2)
            else:
                window_size = min(3, data_length)
            
            # Calculate moving averages
            ma_short = orders_data.tail(window_size).mean()
            ma_long = orders_data.tail(min(window_size * 2, data_length)).mean()
            
            # Detect trend
            if data_length >= 5:
                recent_trend = (orders_data.tail(3).mean() - orders_data.head(3).mean()) / data_length
                trend_adjustment = recent_trend * periods
            else:
                trend_adjustment = 0
            
            # Weighted average of short and long term with trend
            if data_length >= 10:
                forecast_value = (0.7 * ma_short + 0.3 * ma_long) + trend_adjustment
            else:
                forecast_value = ma_short + trend_adjustment
            
            # Calculate confidence based on data stability
            volatility = orders_data.std() / orders_data.mean() if orders_data.mean() > 0 else 1
            confidence = max(0.3, 1 - min(volatility, 1))
            
            return {
                'forecast': forecast_value,
                'confidence': confidence,
                'model_info': {
                    'window_size': window_size,
                    'trend_adjustment': trend_adjustment,
                    'ma_short': ma_short,
                    'ma_long': ma_long
                }
            }
            
        except Exception as e:
            logger.error(f"Moving average forecast failed: {e}")
            return None
    
    def _trend_forecast(self, orders_data: pd.Series, periods: int, 
                       confidence_level: float) -> Dict[str, Any]:
        """
        Simple linear trend forecasting
        """
        try:
            if len(orders_data) < 3:
                # Not enough data for trend analysis
                forecast_value = orders_data.mean()
                confidence = 0.3
            else:
                # Linear regression for trend
                x = np.arange(len(orders_data))
                coefficients = np.polyfit(x, orders_data, 1)
                
                # Forecast future value
                future_x = len(orders_data) + periods - 1
                forecast_value = np.polyval(coefficients, future_x)
                
                # Calculate R-squared for confidence
                y_pred = np.polyval(coefficients, x)
                ss_res = np.sum((orders_data - y_pred) ** 2)
                ss_tot = np.sum((orders_data - orders_data.mean()) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                confidence = max(0.2, min(0.8, r_squared))
            
            return {
                'forecast': forecast_value,
                'confidence': confidence,
                'model_info': {
                    'trend_slope': coefficients[0] if len(orders_data) >= 3 else 0,
                    'r_squared': r_squared if len(orders_data) >= 3 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Trend forecast failed: {e}")
            return None
    
    def _calculate_arima_confidence(self, model_fit, orders_data: pd.Series) -> float:
        """
        Calculate confidence score for ARIMA model
        """
        try:
            # Use AIC and data fit quality
            aic = model_fit.aic
            residuals = model_fit.resid
            
            # Normalize AIC (lower is better)
            aic_score = max(0, 1 - (aic / (len(orders_data) * 10)))
            
            # Residual analysis
            residual_std = residuals.std()
            data_std = orders_data.std()
            residual_score = max(0, 1 - (residual_std / data_std)) if data_std > 0 else 0.5
            
            # Combined confidence
            confidence = (aic_score * 0.3 + residual_score * 0.7)
            return max(0.1, min(0.95, confidence))
            
        except Exception as e:
            logger.error(f"Confidence calculation failed: {e}")
            return 0.5
    
    def _store_forecast_result(self, forecast_value: float, method: str, confidence: float):
        """
        Store forecast result for performance tracking
        """
        try:
            self.last_forecast = forecast_value
            self.forecast_history.append({
                'timestamp': datetime.now(),
                'forecast': forecast_value,
                'method': method,
                'confidence': confidence
            })
            
            # Keep only last 100 forecasts
            if len(self.forecast_history) > 100:
                self.forecast_history = self.forecast_history[-100:]
                
        except Exception as e:
            logger.error(f"Failed to store forecast result: {e}")
    
    def _get_fallback_forecast(self) -> float:
        """
        Ultimate fallback forecast when all methods fail
        """
        if self.last_forecast is not None:
            logger.info(f"Using last successful forecast: {self.last_forecast}")
            return self.last_forecast
        
        if self.forecast_history:
            avg_forecast = np.mean([f['forecast'] for f in self.forecast_history[-5:]])
            logger.info(f"Using average of recent forecasts: {avg_forecast}")
            return avg_forecast
        
        # Default baseline forecast
        default_forecast = 100.0
        logger.info(f"Using default baseline forecast: {default_forecast}")
        return default_forecast
    
    def get_forecast_confidence(self, orders_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze forecast confidence and data quality
        """
        try:
            orders_data, quality_report = self._prepare_and_validate_data(orders_df)
            
            if not quality_report['is_valid']:
                return {
                    'confidence_level': 'Very Low',
                    'confidence_score': 0.1,
                    'data_quality': 'Poor',
                    'issues': quality_report['issues'],
                    'recommendations': ['Improve data quality', 'Collect more data points']
                }
            
            data_length = len(orders_data)
            
            # Data quantity score
            if data_length >= 30:
                quantity_score = 1.0
            elif data_length >= 14:
                quantity_score = 0.8
            elif data_length >= 7:
                quantity_score = 0.6
            else:
                quantity_score = 0.3
            
            # Data quality score
            cv = orders_data.std() / orders_data.mean() if orders_data.mean() > 0 else float('inf')
            if cv < 0.2:
                quality_score = 1.0
            elif cv < 0.5:
                quality_score = 0.8
            elif cv < 1.0:
                quality_score = 0.6
            else:
                quality_score = 0.3
            
            # Model performance score
            total_attempts = sum(perf['total_attempts'] for perf in self.model_performance.values())
            total_successes = sum(perf['success_count'] for perf in self.model_performance.values())
            
            if total_attempts > 0:
                performance_score = total_successes / total_attempts
            else:
                performance_score = 0.7  # Default
            
            # Combined confidence
            overall_confidence = (quantity_score * 0.3 + quality_score * 0.4 + performance_score * 0.3)
            
            # Determine confidence level
            if overall_confidence >= 0.8:
                level = 'High'
            elif overall_confidence >= 0.6:
                level = 'Medium'
            elif overall_confidence >= 0.4:
                level = 'Low'
            else:
                level = 'Very Low'
            
            # Generate recommendations
            recommendations = []
            if data_length < 30:
                recommendations.append(f"Collect more data points (current: {data_length}, recommended: 30+)")
            if cv > 0.5:
                recommendations.append("High variability detected - investigate data patterns")
            if performance_score < 0.7:
                recommendations.append("Consider alternative forecasting methods")
            
            return {
                'confidence_level': level,
                'confidence_score': round(overall_confidence, 3),
                'data_quality': 'Good' if quality_score >= 0.7 else 'Fair' if quality_score >= 0.5 else 'Poor',
                'data_points': data_length,
                'coefficient_of_variation': round(cv, 3),
                'model_performance': round(performance_score, 3),
                'issues': quality_report.get('issues', []),
                'recommendations': recommendations,
                'component_scores': {
                    'data_quantity': round(quantity_score, 3),
                    'data_quality': round(quality_score, 3),
                    'model_performance': round(performance_score, 3)
                }
            }
            
        except Exception as e:
            logger.error(f"Confidence analysis failed: {e}")
            return {
                'confidence_level': 'Unknown',
                'confidence_score': 0.5,
                'data_quality': 'Unknown',
                'error': str(e)
            }
    
    def get_model_performance_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive model performance report
        """
        try:
            report = {
                'total_forecasts': len(self.forecast_history),
                'methods_performance': {},
                'recent_forecasts': self.forecast_history[-10:] if self.forecast_history else [],
                'last_forecast': self.last_forecast
            }
            
            # Calculate performance for each method
            for method, perf in self.model_performance.items():
                if perf['total_attempts'] > 0:
                    success_rate = perf['success_count'] / perf['total_attempts']
                    report['methods_performance'][method] = {
                        'success_rate': round(success_rate, 3),
                        'total_attempts': perf['total_attempts'],
                        'successful_forecasts': perf['success_count']
                    }
            
            # Overall system performance
            total_attempts = sum(perf['total_attempts'] for perf in self.model_performance.values())
            total_successes = sum(perf['success_count'] for perf in self.model_performance.values())
            
            if total_attempts > 0:
                report['overall_success_rate'] = round(total_successes / total_attempts, 3)
            else:
                report['overall_success_rate'] = 0.0
            
            return report
            
        except Exception as e:
            logger.error(f"Performance report generation failed: {e}")
            return {'error': str(e)}

    def reset_performance_tracking(self):
        """Reset performance tracking metrics"""
        self.model_performance = {
            'arima': {'success_count': 0, 'total_attempts': 0},
            'exponential_smoothing': {'success_count': 0, 'total_attempts': 0},
            'seasonal_decompose': {'success_count': 0, 'total_attempts': 0},
            'moving_average': {'success_count': 0, 'total_attempts': 0},
            'trend_forecast': {'success_count': 0, 'total_attempts': 0}
        }
        self.forecast_history = []
        logger.info("Performance tracking reset")