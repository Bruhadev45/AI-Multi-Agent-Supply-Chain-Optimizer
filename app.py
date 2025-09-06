"""
AI Multi-Agent Supply Chain Optimizer - Streamlit Application
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import polyline
import time
import json
from datetime import datetime, timedelta
import logging

# Fix Python path for imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import Orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🚚 AI Supply Chain Optimizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed sidebar CSS only
st.markdown("""
<style>
    .css-1d391kg {
        position: fixed !important;
        height: 100vh !important;
        overflow-y: auto !important;
        z-index: 999 !important;
    }
    .main .block-container {
        padding-left: 1rem;
        max-width: none;
    }
</style>
""", unsafe_allow_html=True)

# Simple header
st.title("🚀 Advanced AI Multi-Agent Supply Chain Optimizer")
st.markdown("**Powered by CrewAI • Real-time Decision Making • Intelligent Orchestration**")

def initialize_session_state():
    """Initialize session state variables"""
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "last_results" not in st.session_state:
        st.session_state.last_results = None
    if "execution_time" not in st.session_state:
        st.session_state.execution_time = None
    if "risk_alerts" not in st.session_state:
        st.session_state.risk_alerts = []

def get_orchestrator():
    """Get or create orchestrator instance"""
    if st.session_state.orchestrator is None:
        try:
            with st.spinner("Initializing AI agents..."):
                st.session_state.orchestrator = Orchestrator()
            return st.session_state.orchestrator
        except Exception as e:
            st.error(f"❌ Failed to initialize orchestrator: {e}")
            st.stop()
    return st.session_state.orchestrator

def get_city_coordinates(city_name):
    """Get coordinates for a city"""
    city_coordinates = {
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
    city_key = city_name.lower().strip()
    return city_coordinates.get(city_key, [23.5, 77.5])  # Default to center of India

def create_route_map(origin: str, destination: str, route_info: dict):
    """Create interactive route map"""
    try:
        # Get coordinates
        origin_coords = get_city_coordinates(origin)
        dest_coords = get_city_coordinates(destination)
        
        # Calculate center point
        center_lat = (origin_coords[0] + dest_coords[0]) / 2
        center_lon = (origin_coords[1] + dest_coords[1]) / 2
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add route line
        if route_info.get("polyline"):
            try:
                points = polyline.decode(route_info["polyline"])
                folium.PolyLine(
                    points, 
                    color="#FF6B6B", 
                    weight=4, 
                    opacity=0.8,
                    tooltip="Optimized Route"
                ).add_to(m)
            except:
                # Fallback: straight line
                folium.PolyLine(
                    [origin_coords, dest_coords],
                    color="#FF6B6B",
                    weight=4,
                    opacity=0.6,
                    tooltip="Direct Route"
                ).add_to(m)
        else:
            # Draw direct line
            folium.PolyLine(
                [origin_coords, dest_coords],
                color="#FF6B6B",
                weight=4,
                opacity=0.6,
                tooltip="Estimated Route"
            ).add_to(m)
        
        # Add markers
        folium.Marker(
            origin_coords,
            popup=f"<b>Origin: {origin}</b><br>🚀 Starting Point",
            tooltip=f"🚀 {origin}",
            icon=folium.Icon(color='green', icon='play', prefix='fa')
        ).add_to(m)
        
        folium.Marker(
            dest_coords,
            popup=f"<b>Destination: {destination}</b><br>🎯 Delivery Point<br>⏱️ ETA: {route_info.get('duration', 'Unknown')}",
            tooltip=f"🎯 {destination}",
            icon=folium.Icon(color='red', icon='flag', prefix='fa')
        ).add_to(m)
        
        return m
        
    except Exception as e:
        logger.error(f"Map creation failed: {e}")
        # Return simple map
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        return m

def get_scenario_config(scenario):
    """Get scenario configuration"""
    scenario_configs = {
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
    return scenario_configs.get(scenario, scenario_configs["🟢 Normal Operations"])

def generate_risk_alerts(results, scenario):
    """Generate risk alerts based on analysis results"""
    alerts = []
    
    # Weather-based alerts
    risk_info = results.get('risk', {})
    if isinstance(risk_info, dict):
        risk_level = risk_info.get('risk_level', '')
        condition = risk_info.get('condition', '')
        
        if 'High' in str(risk_level):
            alerts.append({
                'type': 'high',
                'title': '🌩️ Weather Risk Alert',
                'message': f"High weather risk detected: {condition}. Consider route alternatives or delivery delays.",
                'timestamp': datetime.now()
            })
        elif 'rain' in str(condition).lower() or 'storm' in str(condition).lower():
            alerts.append({
                'type': 'medium',
                'title': '🌧️ Weather Advisory',
                'message': f"Weather condition: {condition}. Monitor closely for potential delays.",
                'timestamp': datetime.now()
            })
    
    # Cost-based alerts
    cost = results.get('best_price', 0)
    route_info = results.get('route_info', {})
    distance = route_info.get('distance_km', 1)
    
    if distance > 0:
        cost_per_km = cost / distance
        if cost_per_km > 5.0:
            alerts.append({
                'type': 'high',
                'title': '💰 High Cost Alert',
                'message': f"Cost per km (₹{cost_per_km:.2f}) exceeds threshold. Review vendor selection.",
                'timestamp': datetime.now()
            })
        elif cost_per_km > 4.0:
            alerts.append({
                'type': 'medium',
                'title': '💸 Cost Advisory',
                'message': f"Above average cost per km (₹{cost_per_km:.2f}). Consider cost optimization.",
                'timestamp': datetime.now()
            })
    
    # Scenario-based alerts
    scenario_risk = get_scenario_config(scenario)['risk_level']
    if scenario_risk == 'High':
        alerts.append({
            'type': 'high',
            'title': '⚠️ Scenario Risk Alert',
            'message': f"Current scenario '{scenario}' carries high operational risk. Implement contingency plans.",
            'timestamp': datetime.now()
        })
    
    # Demand-based alerts
    forecast = results.get('forecast', 0)
    if forecast > 1000:
        alerts.append({
            'type': 'medium',
            'title': '📈 High Demand Alert',
            'message': f"High demand forecast ({forecast:,.0f} orders). Ensure adequate capacity planning.",
            'timestamp': datetime.now()
        })
    
    return alerts

def display_risk_monitor():
    """Display real-time risk monitoring section"""
    st.subheader("🛡️ Real-time Risk Monitor")
    st.markdown("**Continuous monitoring and alerting system**")
    st.markdown("Stay informed about potential risks affecting your supply chain operations.")
    
    if st.session_state.last_results:
        results = st.session_state.last_results
        scenario_used = st.session_state.get("scenario_used", "Unknown")
        
        # Generate current risk alerts
        current_alerts = generate_risk_alerts(results, scenario_used)
        st.session_state.risk_alerts = current_alerts
        
        # Risk Overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_info = results.get('risk', {})
            overall_risk = risk_info.get('risk_level', 'Medium') if isinstance(risk_info, dict) else 'Medium'
            st.metric("🛡️ Overall Risk", overall_risk)
        
        with col2:
            high_alerts = len([a for a in current_alerts if a['type'] == 'high'])
            st.metric("🚨 Active Alerts", f"{len(current_alerts)} Total ({high_alerts} High)")
        
        with col3:
            condition = risk_info.get('condition', 'Unknown') if isinstance(risk_info, dict) else 'Unknown'
            st.metric("🌤️ Weather Risk", condition)
        
        with col4:
            cost = results.get('best_price', 0)
            route_info = results.get('route_info', {})
            distance = route_info.get('distance_km', 1)
            cost_per_km = cost / distance if distance > 0 else 0
            st.metric("💰 Cost per KM", f"₹{cost_per_km:.2f}")
        
        # Active Alerts
        if current_alerts:
            st.subheader("🚨 Active Risk Alerts")
            
            for alert in current_alerts:
                priority = "🔴 HIGH" if alert['type'] == 'high' else "🟡 MEDIUM" if alert['type'] == 'medium' else "🟢 LOW"
                
                with st.expander(f"{priority} - {alert['title']}", expanded=(alert['type'] == 'high')):
                    st.write(alert['message'])
                    st.caption(f"⏰ {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.success("✅ No active risk alerts. All systems operating normally.")
        
        # Risk Trend Chart
        st.subheader("📈 Risk Trend Analysis")
        
        # Generate sample risk trend data
        hours = list(range(24))
        risk_scores = []
        base_score = 30 if 'High' in str(overall_risk) else (20 if 'Medium' in str(overall_risk) else 10)
        
        for hour in hours:
            variation = np.sin(hour / 4) * 10 + np.random.normal(0, 3)
            score = max(0, min(100, base_score + variation))
            risk_scores.append(score)
        
        risk_df = pd.DataFrame({
            'Hour': hours,
            'Risk_Score': risk_scores
        })
        
        fig = px.line(risk_df, x='Hour', y='Risk_Score', title='24-Hour Risk Score Trend')
        fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
        fig.add_hline(y=30, line_dash="dash", line_color="orange", annotation_text="Medium Risk Threshold")
        fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Risk Score", yaxis_range=[0, 100])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk Mitigation
        st.subheader("💡 Risk Mitigation Recommendations")
        
        mitigation_actions = []
        
        if 'High' in str(overall_risk):
            mitigation_actions.extend([
                "🚨 **Immediate Action Required**: Activate contingency protocols",
                "📞 **Communication**: Notify all stakeholders of elevated risk status",
                "🔄 **Alternative Planning**: Prepare backup routes and vendors"
            ])
        
        if high_alerts > 0:
            mitigation_actions.extend([
                "⚠️ **Priority Response**: Address high-priority alerts immediately",
                "📊 **Enhanced Monitoring**: Increase monitoring frequency to 15-minute intervals"
            ])
        
        if not mitigation_actions:
            mitigation_actions = [
                "✅ **Maintain Current Operations**: Continue standard monitoring protocols",
                "📋 **Regular Reviews**: Conduct scheduled risk assessments",
                "🔍 **Proactive Monitoring**: Stay alert for emerging risk factors"
            ]
        
        for action in mitigation_actions:
            st.markdown(f"- {action}")
    
    else:
        st.info("🔄 Run an analysis to activate risk monitoring")
        
        # Demo interface
        st.subheader("📊 Risk Monitoring Dashboard (Demo)")
        demo_cols = st.columns(4)
        with demo_cols[0]:
            st.metric("🛡️ Overall Risk", "Monitoring Ready")
        with demo_cols[1]:
            st.metric("🚨 Active Alerts", "0 Active")
        with demo_cols[2]:
            st.metric("🌤️ Weather Risk", "Awaiting Data")
        with demo_cols[3]:
            st.metric("💰 Cost Risk", "Awaiting Analysis")

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Get orchestrator
    orchestrator = get_orchestrator()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration Panel")
        
        # Route settings
        st.subheader("📍 Route Settings")
        
        indian_cities = [
            "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad",
            "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur",
            "Indore", "Bhopal"
        ]
        
        origin = st.selectbox("Origin City", indian_cities, index=0)
        destination = st.selectbox("Destination City", indian_cities, index=1)
        
        if origin == destination:
            st.warning("⚠️ Origin and destination cannot be the same!")
        
        st.markdown("---")
        
        # Scenario Selection
        st.subheader("🧪 Operational Scenarios")
        
        scenario_options = [
            "🟢 Normal Operations",
            "📈 Peak Season Demand (+40%)",
            "💰 Fuel Price Surge (+25%)",
            "🌪️ Monsoon Disruption",
            "⚡ Emergency Supply",
            "🏭 Industrial Strike"
        ]
        
        scenario = st.radio(
            "Select Scenario:",
            scenario_options,
            index=0,
            key="scenario_selection"
        )
        
        # Show scenario details
        scenario_config = get_scenario_config(scenario)
        st.markdown("**Scenario Impact:**")
        st.markdown(f"- **Demand:** {scenario_config['demand_multiplier']:.1%} of baseline")
        st.markdown(f"- **Cost:** {scenario_config['cost_multiplier']:.1%} of baseline")
        st.markdown(f"- **Risk Level:** {scenario_config['risk_level']}")
        
        st.markdown("---")
        
        # Quick Risk Status
        if st.session_state.last_results:
            st.subheader("🛡️ Quick Risk Status")
            alerts = st.session_state.get('risk_alerts', [])
            high_alerts = len([a for a in alerts if a['type'] == 'high'])
            
            if high_alerts > 0:
                st.error(f"🚨 {high_alerts} High Risk Alert(s)")
            elif len(alerts) > 0:
                st.warning(f"⚠️ {len(alerts)} Active Alert(s)")
            else:
                st.success("✅ All Systems Normal")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            run_button = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
        with col2:
            clear_button = st.button("🗑️ Clear Results", use_container_width=True)
        
        if clear_button:
            st.session_state.last_results = None
            st.session_state.execution_time = None
            st.session_state.risk_alerts = []
            st.success("Results cleared!")
            time.sleep(1)
            st.rerun()
    
    # Main execution logic
    if run_button:
        if origin == destination:
            st.error("❌ Please select different origin and destination cities!")
            st.stop()
        
        # Run comprehensive analysis
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            st.markdown("## 📊 AI Agent Execution Pipeline")
            
            with st.spinner("Executing multi-agent analysis..."):
                status_text.text("🤖 Initializing AI agents...")
                progress_bar.progress(0.1)
                
                # Run analysis
                results = orchestrator.run_comprehensive_analysis(
                    orders_csv=None,
                    origin=origin,
                    destination=destination,
                    scenario=scenario
                )
                
                progress_bar.progress(1.0)
                status_text.text("✅ Analysis completed successfully!")
                
                # Store results
                st.session_state.last_results = results
                st.session_state.execution_time = datetime.now()
                st.session_state.scenario_used = scenario
                
                st.success("🎉 Multi-agent analysis completed successfully!")
                time.sleep(1)
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            logger.error(f"Analysis error: {e}")
    
    # Dashboard section
    if st.session_state.last_results:
        results = st.session_state.last_results
        execution_time = st.session_state.execution_time
        scenario_used = st.session_state.get("scenario_used", "Unknown")
        
        st.markdown("---")
        st.markdown("## 📊 Comprehensive Analytics Dashboard")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            forecast_val = results.get('forecast', 0)
            st.metric("📈 Demand Forecast", f"{forecast_val:,.0f}")
            original_forecast = results.get('forecast_original', forecast_val)
            if original_forecast != forecast_val:
                delta = forecast_val - original_forecast
                st.caption(f"Δ {delta:+.0f} scenario impact")
        
        with col2:
            route_info = results.get('route_info', {})
            distance = route_info.get('distance_km', 0)
            st.metric("🛣️ Route Distance", f"{distance:.0f} km")
            duration = route_info.get('duration', 'Unknown')
            st.caption(f"Duration: {duration}")
        
        with col3:
            price = results.get('best_price', 0)
            st.metric("💰 Optimized Cost", f"₹{price:,.2f}")
            vendor = results.get('best_vendor', 'Unknown')
            st.caption(f"Vendor: {vendor}")
        
        with col4:
            risk = results.get('risk', {})
            risk_level = risk.get('risk_level', 'Medium') if isinstance(risk, dict) else 'Medium'
            clean_risk = risk_level.replace('🔴', 'High').replace('🟡', 'Medium').replace('🟢', 'Low')
            st.metric("⚠️ Risk Level", clean_risk)
            condition = risk.get('condition', 'Unknown') if isinstance(risk, dict) else 'Unknown'
            st.caption(f"Weather: {condition}")
        
        # Detailed Dashboard Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🛡️ Risk Monitor", "📈 Demand Analytics", "🗺️ Route Visualization", "💰 Cost Analysis", "📋 Strategic Summary"])
        
        with tab1:
            display_risk_monitor()
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Demand Forecast Analysis")
                st.markdown("Analyze historical demand patterns and forecast future trends.")

                # Create sample trend data
                dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
                base_demand = 100
                trend_data = [base_demand + np.sin(i/5) * 10 + np.random.normal(0, 5) for i in range(30)]
                
                trend_df = pd.DataFrame({
                    'date': dates,
                    'orders': trend_data
                })
                
                fig = px.line(trend_df, x='date', y='orders', title="Historical Order Patterns")
                
                # Add forecast line
                forecast_val = results.get('forecast', 100)
                fig.add_hline(y=forecast_val, line_dash="dash", line_color="red",
                            annotation_text=f"Forecast: {forecast_val:,.0f}")
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📈 Scenario Impact Comparison")
                
                base_forecast = results.get('forecast_original', 100)
                scenarios = {
                    "Normal": base_forecast,
                    "Peak Season": base_forecast * 1.4,
                    "Fuel Surge": base_forecast,
                    "Monsoon": base_forecast * 0.9,
                    "Emergency": base_forecast * 1.2,
                    "Strike": base_forecast
                }
                
                scenario_df = pd.DataFrame(list(scenarios.items()), columns=['Scenario', 'Demand'])
                
                fig = px.bar(scenario_df, x='Scenario', y='Demand', title="Demand by Scenario",
                           color='Demand', color_continuous_scale='viridis')
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.info(f"**Current Scenario:** {scenario_used}")
        
        with tab3:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("🗺️ Route Visualization")
                st.markdown("Interactive map of the optimized delivery route.")
                route_map = create_route_map(origin, destination, route_info)
                st_folium(route_map, width=700, height=500)
            
            with col2:
                st.subheader("🛣️ Route Details")
                
                st.markdown(f"""
                **From:** {origin}  
                **To:** {destination}  
                **Distance:** {distance:.0f} km  
                **Duration:** {duration}  
                **Source:** {route_info.get('source', 'Unknown')}
                """)
                
                # Route efficiency metrics
                if distance > 0:
                    fuel_estimate = distance / 15  # 15 km/liter
                    co2_estimate = distance * 0.21  # kg CO2 per km
                    
                    st.metric("⛽ Fuel Estimate", f"{fuel_estimate:.1f}L")
                    st.metric("🌱 CO₂ Estimate", f"{co2_estimate:.1f}kg")
                    
                    efficiency_score = min(100, max(0, 100 - (distance / 20)))
                    st.metric("📊 Route Efficiency", f"{efficiency_score:.0f}%")
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 Comprehensive Vendor Analysis")
                vendors = results.get("all_vendors")
                
                if vendors is not None and not vendors.empty:
                    # Create tabs for different vendor analyses
                    vendor_tab1, vendor_tab2, vendor_tab3 = st.tabs(["📊 Overview", "🔍 Detailed Comparison", "🏆 Rankings"])
                    
                    with vendor_tab1:
                        # Vendor count info
                        st.info(f"📊 Analyzing **{len(vendors)} vendors** for your route")
                        
                        # Main vendor comparison table with key metrics
                        key_columns = ['vendor', 'total_cost', 'cost_per_km', 'reliability_score', 
                                     'delivery_speed', 'customer_rating', 'emission_per_km']
                        available_key_cols = [col for col in key_columns if col in vendors.columns]
                        display_vendors = vendors[available_key_cols].copy()
                        
                        # Format the display
                        if 'total_cost' in display_vendors.columns:
                            display_vendors['total_cost'] = display_vendors['total_cost'].apply(lambda x: f"₹{x:,.0f}")
                        if 'cost_per_km' in display_vendors.columns:
                            display_vendors['cost_per_km'] = display_vendors['cost_per_km'].apply(lambda x: f"₹{x:.2f}")
                        if 'emission_per_km' in display_vendors.columns:
                            display_vendors['emission_per_km'] = display_vendors['emission_per_km'].apply(lambda x: f"{x:.2f}kg")
                        if 'customer_rating' in display_vendors.columns:
                            display_vendors['customer_rating'] = display_vendors['customer_rating'].apply(lambda x: f"⭐{x:.1f}")
                        
                        # Rename columns for better display
                        column_names = {
                            'vendor': 'Vendor',
                            'total_cost': 'Total Cost',
                            'cost_per_km': 'Rate/KM',
                            'reliability_score': 'Reliability',
                            'delivery_speed': 'Speed Type',
                            'customer_rating': 'Rating',
                            'emission_per_km': 'CO₂/KM'
                        }
                        
                        display_vendors = display_vendors.rename(columns=column_names)
                        st.dataframe(display_vendors, use_container_width=True)
                        
                        # Quick insights
                        st.subheader("📊 Quick Insights")
                        
                        insights = []
                        
                        if 'total_cost' in vendors.columns:
                            cheapest = vendors.loc[vendors['total_cost'].idxmin(), 'vendor']
                            insights.append(f"💰 **Most Cost-Effective:** {cheapest}")
                        
                        if 'customer_rating' in vendors.columns:
                            highest_rated = vendors.loc[vendors['customer_rating'].idxmax(), 'vendor']
                            insights.append(f"🏆 **Highest Rated:** {highest_rated}")
                        
                        if 'emission_per_km' in vendors.columns:
                            greenest = vendors.loc[vendors['emission_per_km'].idxmin(), 'vendor']
                            insights.append(f"🌱 **Most Eco-Friendly:** {greenest}")
                        
                        if 'max_capacity_kg' in vendors.columns:
                            largest_capacity = vendors.loc[vendors['max_capacity_kg'].idxmax(), 'vendor']
                            insights.append(f"📦 **Largest Capacity:** {largest_capacity}")
                        
                        for insight in insights:
                            st.markdown(f"- {insight}")
                    
                    with vendor_tab2:
                        # Detailed vendor information
                        selected_vendor = st.selectbox(
                            "Select vendor for detailed analysis:",
                            vendors['vendor'].tolist() if 'vendor' in vendors.columns else []
                        )
                        
                        if selected_vendor and 'vendor' in vendors.columns:
                            vendor_details = vendors[vendors['vendor'] == selected_vendor].iloc[0]
                            
                            # Display detailed vendor info in organized sections
                            col_left, col_right = st.columns(2)
                            
                            with col_left:
                                st.markdown("#### 📋 Basic Information")
                                basic_info = {}
                                if 'headquarters_city' in vendor_details:
                                    basic_info['Headquarters'] = vendor_details['headquarters_city']
                                if 'established_year' in vendor_details:
                                    basic_info['Established'] = vendor_details['established_year']
                                if 'fleet_size' in vendor_details:
                                    basic_info['Fleet Size'] = f"{vendor_details['fleet_size']} vehicles"
                                if 'geographic_coverage' in vendor_details:
                                    basic_info['Coverage'] = vendor_details['geographic_coverage']
                                
                                for key, value in basic_info.items():
                                    st.markdown(f"**{key}:** {value}")
                                
                                st.markdown("#### 🚚 Service Details")
                                service_info = {}
                                if 'specialization' in vendor_details:
                                    service_info['Specialization'] = vendor_details['specialization']
                                if 'delivery_speed' in vendor_details:
                                    service_info['Delivery Type'] = vendor_details['delivery_speed']
                                if 'fuel_type' in vendor_details:
                                    service_info['Fuel Type'] = vendor_details['fuel_type']
                                if 'tracking_system' in vendor_details:
                                    service_info['Tracking'] = vendor_details['tracking_system']
                                
                                for key, value in service_info.items():
                                    st.markdown(f"**{key}:** {value}")
                            
                            with col_right:
                                st.markdown("#### 📊 Performance Metrics")
                                metrics = {}
                                if 'reliability_score' in vendor_details:
                                    metrics['Reliability'] = f"{vendor_details['reliability_score']}/10"
                                if 'service_quality' in vendor_details:
                                    metrics['Service Quality'] = f"{vendor_details['service_quality']}/10"
                                if 'customer_rating' in vendor_details:
                                    metrics['Customer Rating'] = f"⭐{vendor_details['customer_rating']}/5"
                                if 'cost_per_km' in vendor_details:
                                    metrics['Rate per KM'] = f"₹{vendor_details['cost_per_km']:.2f}"
                                
                                for key, value in metrics.items():
                                    st.markdown(f"**{key}:** {value}")
                                
                                st.markdown("#### 🛡️ Support & Security")
                                support_info = {}
                                if 'emergency_support' in vendor_details:
                                    support_info['Emergency Support'] = vendor_details['emergency_support']
                                if 'insurance_coverage' in vendor_details:
                                    support_info['Insurance'] = f"₹{vendor_details['insurance_coverage']:,}"
                                if 'certification' in vendor_details:
                                    support_info['Certifications'] = vendor_details['certification']
                                if 'payment_terms' in vendor_details:
                                    support_info['Payment Terms'] = vendor_details['payment_terms']
                                
                                for key, value in support_info.items():
                                    st.markdown(f"**{key}:** {value}")
                            
                            # Contact information
                            if any(col in vendor_details for col in ['contact_phone', 'contact_email']):
                                st.markdown("#### 📞 Contact Information")
                                contact_cols = st.columns(2)
                                if 'contact_phone' in vendor_details:
                                    with contact_cols[0]:
                                        st.markdown(f"**Phone:** {vendor_details['contact_phone']}")
                                if 'contact_email' in vendor_details:
                                    with contact_cols[1]:
                                        st.markdown(f"**Email:** {vendor_details['contact_email']}")
                    
                    with vendor_tab3:
                        # Rankings and comparisons
                        st.markdown("#### 🏆 Vendor Rankings")
                        
                        ranking_cols = st.columns(2)
                        
                        with ranking_cols[0]:
                            # Cost ranking
                            if 'total_cost' in vendors.columns:
                                cost_ranking = vendors.nsmallest(5, 'total_cost')[['vendor', 'total_cost']].copy()
                                cost_ranking['total_cost'] = cost_ranking['total_cost'].apply(lambda x: f"₹{x:,.0f}")
                                cost_ranking.index = range(1, len(cost_ranking) + 1)
                                st.markdown("**💰 Most Cost-Effective**")
                                st.dataframe(cost_ranking.rename(columns={'vendor': 'Vendor', 'total_cost': 'Total Cost'}))
                            
                            # Environmental ranking
                            if 'emission_per_km' in vendors.columns:
                                eco_ranking = vendors.nsmallest(5, 'emission_per_km')[['vendor', 'emission_per_km']].copy()
                                eco_ranking['emission_per_km'] = eco_ranking['emission_per_km'].apply(lambda x: f"{x:.2f} kg/km")
                                eco_ranking.index = range(1, len(eco_ranking) + 1)
                                st.markdown("**🌱 Most Eco-Friendly**")
                                st.dataframe(eco_ranking.rename(columns={'vendor': 'Vendor', 'emission_per_km': 'CO₂ Emission'}))
                        
                        with ranking_cols[1]:
                            # Reliability ranking
                            if 'reliability_score' in vendors.columns:
                                reliability_ranking = vendors.nlargest(5, 'reliability_score')[['vendor', 'reliability_score']].copy()
                                reliability_ranking['reliability_score'] = reliability_ranking['reliability_score'].apply(lambda x: f"{x}/10")
                                reliability_ranking.index = range(1, len(reliability_ranking) + 1)
                                st.markdown("**🛡️ Most Reliable**")
                                st.dataframe(reliability_ranking.rename(columns={'vendor': 'Vendor', 'reliability_score': 'Reliability'}))
                            
                            # Customer rating ranking
                            if 'customer_rating' in vendors.columns:
                                rating_ranking = vendors.nlargest(5, 'customer_rating')[['vendor', 'customer_rating']].copy()
                                rating_ranking['customer_rating'] = rating_ranking['customer_rating'].apply(lambda x: f"⭐{x:.1f}/5")
                                rating_ranking.index = range(1, len(rating_ranking) + 1)
                                st.markdown("**⭐ Highest Rated**")
                                st.dataframe(rating_ranking.rename(columns={'vendor': 'Vendor', 'customer_rating': 'Rating'}))
                
                else:
                    st.warning("📊 Vendor data not available for this analysis")
            
            with col2:
                st.subheader("📊 Cost Analysis & Breakdown")
                
                total_cost = results.get('best_price', 0)
                if total_cost > 0:
                    # Cost components
                    components = {
                        'Transportation': total_cost * 0.60,
                        'Fuel': total_cost * 0.25,
                        'Insurance': total_cost * 0.08,
                        'Tolls': total_cost * 0.05,
                        'Service Fee': total_cost * 0.02
                    }
                    
                    fig = px.pie(
                        values=list(components.values()),
                        names=list(components.keys()),
                        title="Cost Structure Breakdown"
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Cost metrics
                    st.subheader("💰 Cost Summary")
                    
                    distance = route_info.get('distance_km', 1)
                    cost_per_km = total_cost / distance if distance > 0 else 0
                    total_with_gst = total_cost * 1.18
                    
                    metric_col1, metric_col2 = st.columns(2)
                    
                    with metric_col1:
                        st.metric("📏 Cost per KM", f"₹{cost_per_km:.2f}")
                        st.metric("💰 Base Cost", f"₹{total_cost:,.2f}")
                    
                    with metric_col2:
                        st.metric("📋 Total + GST (18%)", f"₹{total_with_gst:,.2f}")
                        st.metric("📊 Distance", f"{distance:.0f} km")
                
                else:
                    st.warning("💰 Cost breakdown not available")
                    
                # Cost insights
                st.subheader("💡 Cost Insights")
                vendor = results.get('best_vendor', 'Unknown')
                if vendor != 'Unknown':
                    st.info(f"**Selected Vendor:** {vendor}")
                    st.info(f"**Route Distance:** {distance:.0f} km")
                    if total_cost > 0:
                        st.success(f"**Optimized Rate:** ₹{cost_per_km:.2f}/km")
                        
                        # Cost comparison
                        if cost_per_km < 3.0:
                            st.success("✅ Excellent rate - below ₹3/km")
                        elif cost_per_km < 4.0:
                            st.info("ℹ️ Good rate - competitive pricing")
                        else:
                            st.warning("⚠️ Premium rate - consider alternatives")
        
        with tab5:
            st.subheader("📋 Strategic Summary & Recommendations")
            st.markdown("Comprehensive overview and actionable insights for decision-making.")            
            # Executive Summary
            st.subheader("🎯 Executive Summary")
            
            summary_data = {
                'scenario': scenario_used,
                'route': f"{origin} → {destination}",
                'distance': f"{distance:.0f} km",
                'duration': duration,
                'demand': f"{forecast_val:,.0f} orders",
                'vendor': vendor,
                'cost': f"₹{price:,.2f}",
                'risk_level': risk_level
            }
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Operation Details**")
                st.markdown(f"- **Scenario:** {summary_data['scenario']}")
                st.markdown(f"- **Route:** {summary_data['route']}")
                st.markdown(f"- **Distance:** {summary_data['distance']}")
                st.markdown(f"- **Duration:** {summary_data['duration']}")
                
            with col2:
                st.markdown("**💼 Business Metrics**")
                st.markdown(f"- **Expected Demand:** {summary_data['demand']}")
                st.markdown(f"- **Selected Vendor:** {summary_data['vendor']}")
                st.markdown(f"- **Total Cost:** {summary_data['cost']}")
                st.markdown(f"- **Risk Level:** {summary_data['risk_level']}")
            
            st.markdown("---")
            
            # Strategic Insights
            st.subheader("💡 Strategic Insights & Recommendations")
            
            final_reasoning = results.get('crew_reasoning', 'Strategic analysis completed by AI agents')
            
            if final_reasoning and len(final_reasoning) > 100:
                with st.expander("📖 View Detailed Strategic Analysis", expanded=True):
                    st.markdown(final_reasoning)
            else:
                st.info(final_reasoning)
            
            st.markdown("---")
            
            # Action Items
            st.subheader("✅ Recommended Action Items")
            
            action_items = [
                f"**Immediate:** Confirm booking with {vendor} for route optimization",
                f"**Preparation:** Ensure inventory capacity for {forecast_val:,.0f} orders",
                f"**Monitoring:** Track delivery performance and cost efficiency",
                f"**Risk Management:** Monitor weather conditions for {destination}",
                f"**Follow-up:** Review performance metrics post-delivery"
            ]
            
            for i, item in enumerate(action_items, 1):
                st.markdown(f"{i}. {item}")
            
            st.markdown("---")
            
            # Export
            st.subheader("📤 Export Analysis Data")
            
            export_data = {
                "analysis_timestamp": execution_time.isoformat() if execution_time else datetime.now().isoformat(),
                "scenario": scenario_used,
                "route_analysis": summary_data,
                "strategic_recommendations": final_reasoning,
                "agent_results": {
                    "demand_forecast": results.get('forecast', 0),
                    "route_optimization": results.get('route_info', {}),
                    "cost_analysis": results.get('best_price', 0),
                    "weather_assessment": results.get('risk', {}),
                    "vendor_recommendation": results.get('best_vendor', 'Unknown')
                }
            }
            
            col1, col2 = st.columns(2)
            
            with col1:
                json_data = json.dumps(export_data, indent=2, default=str)
                st.download_button(
                    "📄 Download Full Report (JSON)",
                    json_data,
                    file_name=f"supply_chain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                vendors = results.get("all_vendors")
                if vendors is not None and not vendors.empty:
                    csv_data = vendors.to_csv(index=False)
                    st.download_button(
                        "📊 Download Vendor Data (CSV)",
                        csv_data,
                        file_name=f"vendor_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("Vendor data not available for CSV export")
            
            st.markdown("**💡 Tip:** Use JSON for complete analysis or CSV for vendor comparison data.")
    
    # Risk Monitor as separate section when no results
    else:
        st.markdown("---")
        st.info("👆 Configure your route settings and operational scenario in the sidebar, then click '🚀 Run Analysis' to begin.")

    
    # Footer
    st.markdown("---")
    st.subheader("🔧 System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🤖 AI Multi-Agent System**")
        st.markdown("- 5 Specialized AI Agents")
        st.markdown("- CrewAI Orchestration")
        st.markdown("- Real-time Decision Making")
        st.markdown("- Scenario-based Analysis")
    
    with col2:
        st.markdown("**🔧 Integration & APIs**")
        st.markdown("- OpenAI GPT-4 Reasoning")
        st.markdown("- Google Maps Navigation")
        st.markdown("- WeatherAPI Monitoring")
        st.markdown("- Dynamic Route Optimization")
    
    with col3:
        st.markdown("**📊 Key Capabilities**")
        st.markdown("- ARIMA Demand Forecasting")
        st.markdown("- Multi-Vendor Cost Analysis")
        st.markdown("- Weather Risk Assessment")
        st.markdown("- Strategic Recommendations")
    
    st.markdown("---")
    st.markdown("**🚀 AI Supply Chain Optimizer • Built with Multi-Agent Systems**")
    st.markdown("*Powered by CrewAI • Streamlit • OpenAI GPT-4 • Google Maps API • WeatherAPI*")

if __name__ == "__main__":
    main()
