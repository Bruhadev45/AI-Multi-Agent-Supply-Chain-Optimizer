import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import polyline
import time
import json
import requests
from datetime import datetime, timedelta

from orchestrator import Orchestrator
import logging
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

# Custom CSS for better styling
st.markdown("""
<style>
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4ECDC4;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .scenario-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e9ecef;
        margin: 0.5rem 0;
    }
    .scenario-card:hover {
        border-color: #4ECDC4;
        background: #e8f5e8;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 Advanced AI Multi-Agent Supply Chain Optimizer</h1>
    <p>Powered by CrewAI • Real-time Decision Making • Intelligent Orchestration</p>
</div>
""", unsafe_allow_html=True)

# City coordinates for dynamic map markers
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
    'bhopal': [23.2599, 77.4126],
    'visakhapatnam': [17.6868, 83.2185],
    'patna': [25.5941, 85.1376],
    'vadodara': [22.3072, 73.1812],
    'ghaziabad': [28.6692, 77.4538],
    'ludhiana': [30.9010, 75.8573],
    'coimbatore': [11.0168, 76.9558]
}

def get_city_coordinates(city_name):
    """Get coordinates for a city"""
    city_key = city_name.lower().strip()
    return CITY_COORDINATES.get(city_key, [23.5, 77.5])  # Default to center of India

def create_sample_data():
    """Create sample data if files don't exist"""
    try:
        # Sample orders data with seasonal patterns
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        base_orders = 100
        seasonal_pattern = [base_orders + 10 * np.sin(2 * np.pi * i / 365) for i in range(len(dates))]
        random_variation = np.random.normal(0, 8, len(dates))
        orders_data = {
            'date': dates,
            'orders': [max(50, int(s + r)) for s, r in zip(seasonal_pattern, random_variation)]
        }
        orders_df = pd.DataFrame(orders_data)
        
        # Sample vendors data
        vendors_data = {
            'vendor': ['LogiTech Express', 'GreenShip Co', 'FastTrack Logistics', 'EcoFreight', 'SpeedyDelivery'],
            'cost_per_km': [2.5, 3.2, 2.8, 3.5, 2.3],
            'emission_per_km': [0.8, 0.3, 0.6, 0.2, 0.9],
            'reliability_score': [8.5, 9.2, 7.8, 9.5, 7.2],
            'delivery_speed': ['Standard', 'Eco', 'Fast', 'Eco+', 'Express']
        }
        vendors_df = pd.DataFrame(vendors_data)
        
        return orders_df, vendors_df
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration Panel")
    
    # Route settings
    st.subheader("📍 Route Settings")
    
    # Popular Indian cities for dropdown
    indian_cities = [
        "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", 
        "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur",
        "Indore", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad",
        "Ludhiana", "Coimbatore"
    ]
    
    origin = st.selectbox("Origin City", indian_cities, index=0)
    destination = st.selectbox("Destination City", indian_cities, index=1)
    
    if origin == destination:
        st.warning("⚠️ Origin and destination cannot be the same!")
    
    st.markdown("---")
    
    # Enhanced Scenario Simulation
    st.subheader("🧪 Operational Scenarios")
    
    scenario_descriptions = {
        "🟢 Normal Operations": {
            "desc": "Standard supply chain operations with regular demand patterns",
            "impact": "Baseline performance metrics",
            "demand_mult": 1.0,
            "cost_mult": 1.0,
            "risk": "Low"
        },
        "📈 Peak Season Demand (+40%)": {
            "desc": "Holiday season or festival period with increased orders",
            "impact": "Higher inventory needs, potential capacity constraints",
            "demand_mult": 1.4,
            "cost_mult": 1.1,
            "risk": "Medium"
        },
        "💰 Fuel Price Surge (+25%)": {
            "desc": "Rising fuel costs affecting transportation expenses",
            "impact": "Increased logistics costs, route optimization crucial",
            "demand_mult": 1.0,
            "cost_mult": 1.25,
            "risk": "Medium"
        },
        "🌪️ Monsoon Disruption": {
            "desc": "Weather-related delays and route complications",
            "impact": "Extended delivery times, higher risk factors",
            "demand_mult": 0.9,
            "cost_mult": 1.15,
            "risk": "High"
        },
        "⚡ Emergency Supply": {
            "desc": "Urgent delivery requirements with time constraints",
            "impact": "Premium costs, expedited processing needed",
            "demand_mult": 1.2,
            "cost_mult": 1.3,
            "risk": "Medium"
        },
        "🏭 Industrial Strike": {
            "desc": "Labor disruptions affecting vendor availability",
            "impact": "Limited vendor options, potential delays",
            "demand_mult": 1.0,
            "cost_mult": 1.2,
            "risk": "High"
        }
    }
    
    scenario = st.radio("Select Scenario:", list(scenario_descriptions.keys()))
    
    # Show scenario details
    scenario_info = scenario_descriptions[scenario]
    with st.expander(f"ℹ️ {scenario} Details"):
        st.markdown(f"""
        **Description:** {scenario_info['desc']}
        
        **Business Impact:** {scenario_info['impact']}
        
        **Adjustments:**
        - Demand: {scenario_info['demand_mult']:.1%} of baseline
        - Cost: {scenario_info['cost_mult']:.1%} of baseline  
        - Risk Level: {scenario_info['risk']}
        """)
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear All", use_container_width=True)
    
    # Clear all functionality
    if clear_button:
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # System status
    st.subheader("🔍 System Status")
    status_placeholder = st.empty()

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    return Orchestrator()

try:
    orchestrator = get_orchestrator()
    status_placeholder.success("✅ All agents operational")
except Exception as e:
    status_placeholder.error(f"❌ System error: {str(e)}")
    st.stop()

# Main execution logic
if run_button:
    if origin == destination:
        st.error("❌ Please select different origin and destination cities!")
        st.stop()
    
    try:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        st.markdown("## 📊 AI Agent Execution Pipeline")
        
        # Create containers for real-time updates
        agent_containers = {
            'forecast': st.empty(),
            'route': st.empty(),
            'cost': st.empty(),
            'risk': st.empty(),
            'coordinator': st.empty()
        }
        
        results = {}
        total_steps = 5
        scenario_info = scenario_descriptions[scenario]
        
        # Step 1: Demand Forecast Agent
        progress_bar.progress(1/total_steps)
        status_text.text("🔮 Demand Forecast Agent analyzing patterns...")
        
        with agent_containers['forecast'].container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.subheader("🔮 Demand Forecast Agent")
            forecast_progress = st.progress(0)
            
            # Simulate processing time
            for i in range(3):
                forecast_progress.progress((i+1)/3)
                time.sleep(0.3)
            
            try:
                # Try to load real data, fall back to sample data
                try:
                    orders = pd.read_csv("data/orders.csv")
                except:
                    orders = create_sample_data()[0]
                    
                forecast = orchestrator.demand_agent.forecast(orders)
                
                # Apply scenario multiplier
                forecast_adjusted = forecast * scenario_info['demand_mult']
                
                results["forecast"] = forecast_adjusted
                results["forecast_original"] = forecast
                results["orders"] = orders
                
                col1, col2, col3 = st.columns(3)
                col1.metric("📈 Base Forecast", f"{forecast:,.0f}")
                col2.metric("🎯 Scenario Adjusted", f"{forecast_adjusted:,.0f}")
                col3.metric("📊 Historical Avg", f"{orders['orders'].mean():.0f}")
                
                st.success(f"✅ Forecast Complete: {forecast_adjusted:,.0f} orders predicted")
                
            except Exception as e:
                st.error(f"❌ Forecast failed: {str(e)}")
                results["forecast"] = 120  # fallback
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 2: Route Optimization Agent
        progress_bar.progress(2/total_steps)
        status_text.text("🗺️ Route Optimizer Agent finding optimal path...")
        
        with agent_containers['route'].container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.subheader("🗺️ Route Optimization Agent")
            route_progress = st.progress(0)
            
            for i in range(3):
                route_progress.progress((i+1)/3)
                time.sleep(0.3)
            
            try:
                route_info = orchestrator.route_agent.get_best_route(origin, destination)
                results["route_info"] = route_info
                
                col1, col2, col3 = st.columns(3)
                col1.metric("🛣️ Distance", f"{route_info['distance_km']:.1f} km")
                col2.metric("⏱️ Duration", route_info['duration'])
                col3.metric("🔌 Data Source", route_info['source'])
                
                st.success(f"✅ Route Optimized: {origin} → {destination}")
                
            except Exception as e:
                st.error(f"❌ Route optimization failed: {str(e)}")
                # Fallback route info
                results["route_info"] = {
                    "path": [origin, destination], 
                    "distance_km": 1400, 
                    "duration": "18 hours",
                    "source": "Fallback estimation",
                    "polyline": None
                }
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 3: Cost Analyzer Agent
        progress_bar.progress(3/total_steps)
        status_text.text("💰 Cost Analyzer Agent evaluating vendors...")
        
        with agent_containers['cost'].container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.subheader("💰 Cost Analyzer Agent")
            cost_progress = st.progress(0)
            
            for i in range(3):
                cost_progress.progress((i+1)/3)
                time.sleep(0.3)
            
            try:
                # Get vendor analysis
                vendor, price, all_vendors = orchestrator.cost_agent.compare_vendors(
                    results["route_info"]["distance_km"]
                )
                
                # Apply scenario cost multiplier
                price_adjusted = price * scenario_info['cost_mult']
                if not all_vendors.empty:
                    all_vendors['total_cost'] = all_vendors['total_cost'] * scenario_info['cost_mult']
                
                results["best_vendor"] = vendor
                results["best_price"] = price_adjusted
                results["original_price"] = price
                results["all_vendors"] = all_vendors
                
                col1, col2, col3 = st.columns(3)
                col1.metric("🏆 Best Vendor", vendor)
                col2.metric("💳 Scenario Cost", f"₹{price_adjusted:,.2f}")
                col3.metric("📊 Base Cost", f"₹{price:,.2f}")
                
                st.success(f"✅ Cost Analysis: {vendor} selected @ ₹{price_adjusted:,.2f}")
                
            except Exception as e:
                st.error(f"❌ Cost analysis failed: {str(e)}")
                results["best_vendor"] = "Fallback Vendor"
                results["best_price"] = 5000
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 4: Risk Monitor Agent
        progress_bar.progress(4/total_steps)
        status_text.text("⚠️ Risk Monitor Agent assessing conditions...")
        
        with agent_containers['risk'].container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.subheader("⚠️ Risk Monitor Agent")
            risk_progress = st.progress(0)
            
            for i in range(3):
                risk_progress.progress((i+1)/3)
                time.sleep(0.3)
            
            try:
                risk = orchestrator.risk_agent.check_weather(destination)
                
                # Override risk for specific scenarios
                if "Monsoon" in scenario or "Weather" in scenario:
                    risk = {
                        "condition": "Heavy Rain",
                        "temp": "22°C",
                        "humidity": "85%",
                        "wind": "25 km/h",
                        "risk_level": "🔴 High",
                        "scenario_override": True
                    }
                elif "Strike" in scenario:
                    if isinstance(risk, dict):
                        risk["risk_level"] = "🔴 High"
                        risk["additional_risk"] = "Labor disruption"
                
                results["risk"] = risk
                
                if isinstance(risk, dict) and "condition" in risk:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("🌤️ Weather", risk.get("condition", "Unknown"))
                    col2.metric("🌡️ Temp", risk.get("temp", "N/A"))
                    col3.metric("💧 Humidity", risk.get("humidity", "N/A"))
                    col4.metric("🌬️ Wind", risk.get("wind", "N/A"))
                    
                    # Risk level display
                    risk_level = risk.get("risk_level", "🟡 Medium")
                    if "🔴" in risk_level:
                        st.error(f"⚠️ {risk_level}")
                    elif "🟡" in risk_level:
                        st.warning(f"⚠️ {risk_level}")
                    else:
                        st.success(f"✅ {risk_level}")
                        
                    # Additional scenario risks
                    if risk.get("scenario_override"):
                        st.info("🎭 Risk adjusted for selected scenario")
                    if risk.get("additional_risk"):
                        st.warning(f"➕ Additional Risk: {risk['additional_risk']}")
                else:
                    st.warning(f"⚠️ Weather data: {str(risk)}")
                
                st.success("✅ Risk assessment completed")
                
            except Exception as e:
                st.error(f"❌ Risk assessment failed: {str(e)}")
                results["risk"] = {"condition": "Unknown", "risk_level": "🟡 Medium"}
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Step 5: Coordinator Agent (Fixed)
        progress_bar.progress(2/total_steps)
        status_text.text("🎯 Coordinator Agent synthesizing insights...")
        
        with agent_containers['coordinator'].container():
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.subheader("🎯 Strategic Coordinator Agent")
            coord_progress = st.progress(0)
            
            for i in range(4):
                coord_progress.progress((i+1)/4)
                time.sleep(0.4)
            
            try:
                # Fixed: Call the enhanced orchestrator method properly
                comprehensive_results = orchestrator.run_comprehensive_analysis(
                    "data/orders.csv" if pd.io.common.file_exists("data/orders.csv") else None,
                    origin, 
                    destination, 
                    scenario
                )
                
                # Extract the strategic recommendations
                final = comprehensive_results.get("crew_reasoning", "Strategic analysis completed")
                agent_insights = comprehensive_results.get("agent_insights", {})
                
                results["crew_reasoning"] = final
                results["agent_insights"] = agent_insights
                results["system_metadata"] = comprehensive_results.get("execution_metadata", {})
                
                # Display clear strategic summary
                st.markdown("### 🎯 Strategic Recommendations")
                
                # Create a clear, structured summary
                summary_parts = []
                summary_parts.append(f"**🎬 Scenario:** {scenario}")
                summary_parts.append(f"**🛣️ Route:** {origin} → {destination} ({results['route_info']['distance_km']:.0f} km)")
                summary_parts.append(f"**📈 Expected Orders:** {results['forecast']:,.0f}")
                summary_parts.append(f"**🏆 Recommended Vendor:** {results['best_vendor']}")
                summary_parts.append(f"**💰 Total Cost:** ₹{results['best_price']:,.2f}")
                
                risk_info = results['risk']
                if isinstance(risk_info, dict):
                    risk_level = risk_info.get('risk_level', '🟡 Medium')
                    summary_parts.append(f"**⚠️ Risk Level:** {risk_level}")
                
                # Executive summary
                exec_summary = f"""
                ## 📋 Executive Summary
                
                {chr(10).join(summary_parts)}
                
                ## 🎯 Key Insights
                {final}
                
                ## ✅ Recommended Actions
                1. **Immediate:** Confirm booking with {results['best_vendor']} for ₹{results['best_price']:,.2f}
                2. **Monitor:** Track weather conditions and traffic updates for {destination}
                3. **Prepare:** Ensure inventory levels meet forecasted demand of {results['forecast']:,.0f} orders
                4. **Backup:** Maintain alternative vendor contacts for risk mitigation
                5. **Review:** Schedule delivery performance review post-completion
                """
                
                st.markdown(exec_summary)
                st.success("✅ Strategic coordination completed successfully")
                
            except Exception as e:
                st.error(f"❌ Coordination failed: {str(e)}")
                logger.error(f"Coordination error details: {e}")
                
                # Provide fallback strategic summary
                fallback_summary = f"""
                ## 📋 Strategic Summary (Fallback)
                
                **Route Analysis:** {origin} → {destination} ({results.get('route_info', {}).get('distance_km', 'N/A')} km)
                
                **Cost Optimization:** {results.get('best_vendor', 'Unknown')} selected at ₹{results.get('best_price', 0):,.2f}
                
                **Demand Planning:** Prepare for {results.get('forecast', 0):,.0f} orders
                
                **Risk Management:** Monitor conditions and maintain contingency plans
                
                **Recommendation:** Proceed with selected vendor while monitoring risk factors
                """
                
                results["crew_reasoning"] = fallback_summary
                st.markdown(fallback_summary)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        progress_bar.progress(1.0)
        status_text.text("✅ All agents completed successfully!")
        
        # Store results for dashboard
        st.session_state["last_results"] = results
        st.session_state["execution_time"] = datetime.now()
        st.session_state["scenario_used"] = scenario
        
        time.sleep(1)
        
    except Exception as e:
        st.error(f"⚠️ Pipeline execution failed: {str(e)}")
        logger.error(f"Pipeline error: {e}")

# Dashboard section - Enhanced
if "last_results" in st.session_state:
    results = st.session_state["last_results"]
    execution_time = st.session_state.get("execution_time", datetime.now())
    scenario_used = st.session_state.get("scenario_used", "Unknown")
    
    st.markdown("---")
    st.markdown("## 📊 Comprehensive Analytics Dashboard")
    
    # Enhanced metrics with scenario context
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        forecast_val = results.get('forecast', 0)
        st.metric("📈 Demand Forecast", f"{forecast_val:,.0f}" if forecast_val else "N/A")
        if results.get('forecast_original'):
            delta = forecast_val - results['forecast_original']
            st.caption(f"Δ {delta:+.0f} from baseline")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        route_info = results.get('route_info', {})
        distance = route_info.get('distance_km', 0)
        st.metric("🛣️ Route Distance", f"{distance:.0f} km" if distance else "N/A")
        if distance:
            st.caption(f"≈ {distance/50:.1f} hours drive time")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        price = results.get('best_price', 0)
        st.metric("💰 Optimized Cost", f"₹{price:,.2f}" if price else "N/A")
        if results.get('original_price'):
            delta = price - results['original_price']
            st.caption(f"Δ ₹{delta:+.0f} scenario impact")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        risk = results.get('risk', {})
        if isinstance(risk, dict):
            risk_level = risk.get('risk_level', '🟡 Medium')
            clean_risk = risk_level.replace('🔴', 'High').replace('🟡', 'Medium').replace('🟢', 'Low')
            st.metric("⚠️ Risk Level", clean_risk)
            weather = risk.get('condition', 'Unknown')
            st.caption(f"Weather: {weather}")
        else:
            st.metric("⚠️ Risk Level", "Unknown")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main dashboard with enhanced tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Demand Analytics", "🗺️ Route Visualization", "💰 Cost Analysis", "📋 Strategic Summary"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Demand Forecast Trends")
            try:
                orders = results.get("orders")
                if orders is not None and not orders.empty:
                    fig = px.line(orders, x="date", y="orders", 
                                 title="Historical Order Patterns",
                                 markers=True)
                    
                    # Add forecast line
                    forecast_val = results.get('forecast', 0)
                    if forecast_val:
                        fig.add_hline(y=forecast_val, line_dash="dash", 
                                    line_color="red",
                                    annotation_text=f"Forecast: {forecast_val:,.0f}")
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("📊 Order data not available")
            except Exception as e:
                st.error(f"Chart error: {e}")
        
        with col2:
            st.subheader("📈 Scenario Impact Analysis")
            try:
                base_forecast = results.get('forecast_original', results.get('forecast', 100))
                scenarios_impact = {
                    "Normal": base_forecast,
                    "Peak Season (+40%)": base_forecast * 1.4,
                    "Fuel Surge": base_forecast,
                    "Monsoon (-10%)": base_forecast * 0.9,
                    "Emergency (+20%)": base_forecast * 1.2,
                    "Strike": base_forecast
                }
                
                impact_df = pd.DataFrame(list(scenarios_impact.items()), 
                                       columns=['Scenario', 'Demand'])
                
                fig = px.bar(impact_df, x='Scenario', y='Demand',
                           title="Demand Impact by Scenario",
                           color='Demand', color_continuous_scale='viridis')
                
                # Highlight current scenario
                current_scenario_short = scenario_used.split()[1] if len(scenario_used.split()) > 1 else "Normal"
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info(f"Current scenario: **{scenario_used}**")
            except Exception as e:
                st.error(f"Scenario analysis error: {e}")
    
    with tab2:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("🗺️ Optimized Route Map")
            try:
                route_info = results.get('route_info', {})
                
                # Get actual coordinates for origin and destination
                origin_coords = get_city_coordinates(route_info.get('path', ['Mumbai', 'Delhi'])[0])
                dest_coords = get_city_coordinates(route_info.get('path', ['Mumbai', 'Delhi'])[1])
                
                # Calculate map center
                center_lat = (origin_coords[0] + dest_coords[0]) / 2
                center_lon = (origin_coords[1] + dest_coords[1]) / 2
                
                # Create map with satellite tiles
                m = folium.Map(
                    location=[center_lat, center_lon], 
                    zoom_start=6,
                    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='Esri'
                )
                
                # Add route polyline if available
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
                        # Fallback: draw straight line
                        folium.PolyLine(
                            [origin_coords, dest_coords],
                            color="#FF6B6B",
                            weight=4,
                            opacity=0.6,
                            tooltip="Direct Route (Approximate)"
                        ).add_to(m)
                
                # Add dynamic markers with proper coordinates
                path = route_info.get("path", [origin, destination])
                if len(path) >= 2:
                    # Origin marker
                    folium.Marker(
                        origin_coords,
                        popup=f"""
                        <b>Origin: {path[0]}</b><br>
                        📍 Starting Point<br>
                        🚚 Departure Hub
                        """,
                        tooltip=f"🚀 {path[0]}",
                        icon=folium.Icon(color='green', icon='play', prefix='fa')
                    ).add_to(m)
                    
                    # Destination marker
                    folium.Marker(
                        dest_coords,
                        popup=f"""
                        <b>Destination: {path[1]}</b><br>
                        🎯 Delivery Point<br>
                        📦 Customer Location<br>
                        ⏱️ ETA: {route_info.get('duration', 'Calculating...')}
                        """,
                        tooltip=f"🎯 {path[1]}",
                        icon=folium.Icon(color='red', icon='flag', prefix='fa')
                    ).add_to(m)
                
                # Add layer control for different map views
                folium.TileLayer('OpenStreetMap').add_to(m)
                folium.TileLayer(
                    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
                    attr='Esri',
                    name='Street Map'
                ).add_to(m)
                folium.LayerControl().add_to(m)
                
                st_folium(m, width=800, height=500)
                
            except Exception as e:
                st.error(f"🗺️ Map rendering failed: {e}")
                st.info("💡 Map requires valid city names and coordinates")
        
        with col2:
            st.subheader("🛣️ Route Intelligence")
            route_info = results.get('route_info', {})
            
            if route_info:
                # Route details card
                st.markdown(f"""
                <div style="background: #0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4>📍 Route Details</h4>
                <p><b>From:</b> {route_info.get('path', ['N/A', 'N/A'])[0]}</p>
                <p><b>To:</b> {route_info.get('path', ['N/A', 'N/A'])[1]}</p>
                <p><b>Distance:</b> {route_info.get('distance_km', 'N/A')} km</p>
                <p><b>Duration:</b> {route_info.get('duration', 'N/A')}</p>
                <p><b>Source:</b> {route_info.get('source', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Route efficiency metrics
                distance = route_info.get('distance_km', 0)
                if distance and distance > 0:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        fuel_estimate = distance / 15  # Assuming 15 km/liter
                        st.metric("⛽ Fuel Est.", f"{fuel_estimate:.1f}L")
                    with col_b:
                        co2_estimate = distance * 0.21  # kg CO2 per km
                        st.metric("🌱 CO₂ Est.", f"{co2_estimate:.1f}kg")
                    
                    # Efficiency score
                    efficiency_score = min(100, max(0, 100 - (distance / 20)))
                    st.metric("📊 Route Efficiency", f"{efficiency_score:.0f}%")
                
                # Traffic and timing insights
                st.markdown("### ⏰ Timing Insights")
                current_hour = datetime.now().hour
                if 6 <= current_hour <= 10 or 17 <= current_hour <= 21:
                    st.warning("🚦 Peak traffic hours - expect delays")
                else:
                    st.success("✅ Optimal travel time")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Vendor Cost Analysis")
            try:
                vendors = results.get("all_vendors")
                if vendors is not None and not vendors.empty:
                    # Enhanced styling for vendor table
                    def highlight_best(s):
                        is_min = s == s.min()
                        return ['background-color: lightgreen' if v else '' for v in is_min]
                    
                    styled_vendors = vendors.style.apply(highlight_best, subset=['total_cost'])
                    
                    if 'co2_emission' in vendors.columns:
                        styled_vendors = styled_vendors.apply(highlight_best, subset=['co2_emission'])
                    
                    # Format columns
                    format_dict = {
                        "total_cost": "₹{:,.2f}",
                        "cost_per_km": "₹{:.2f}/km",
                        "emission_per_km": "{:.2f} kg/km"
                    }
                    
                    if 'co2_emission' in vendors.columns:
                        format_dict["co2_emission"] = "{:.1f} kg"
                    
                    styled_vendors = styled_vendors.format(format_dict)
                    
                    st.dataframe(styled_vendors, use_container_width=True)
                    
                    # Cost vs Sustainability analysis
                    if 'co2_emission' in vendors.columns and len(vendors) > 1:
                        fig = px.scatter(
                            vendors, 
                            x="total_cost", 
                            y="co2_emission",
                            size="reliability_score" if "reliability_score" in vendors.columns else None,
                            color="vendor",
                            title="Cost vs Environmental Impact Trade-off",
                            labels={
                                "total_cost": "Total Cost (₹)",
                                "co2_emission": "CO₂ Emissions (kg)"
                            },
                            hover_data=["delivery_speed"] if "delivery_speed" in vendors.columns else None
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("📊 Vendor data not available")
            except Exception as e:
                st.error(f"Vendor analysis error: {e}")
        
        with col2:
            st.subheader("📊 Cost Breakdown & Insights")
            
            try:
                best_price = results.get('best_price', 0)
                original_price = results.get('original_price', best_price)
                
                if best_price and best_price > 0:
                    # Cost components
                    components = {
                        'Base Transportation': original_price * 0.60,
                        'Fuel Costs': original_price * 0.25,
                        'Insurance & Safety': original_price * 0.08,
                        'Tolls & Permits': original_price * 0.05,
                        'Service Charges': original_price * 0.02
                    }
                    
                    # Scenario impact
                    scenario_impact = best_price - original_price
                    if abs(scenario_impact) > 1:
                        components[f'Scenario Impact ({scenario_used.split()[0]})'] = scenario_impact
                    
                    # Create pie chart
                    fig = px.pie(
                        values=list(components.values()),
                        names=list(components.keys()),
                        title="Cost Structure Analysis"
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Cost metrics
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("💳 Base Cost", f"₹{original_price:,.2f}")
                        st.metric("📈 Final Cost", f"₹{best_price:,.2f}")
                    with col_b:
                        tax_amount = best_price * 0.18
                        st.metric("💰 Total + GST", f"₹{(best_price + tax_amount):,.2f}")
                        
                        if abs(scenario_impact) > 1:
                            st.metric("🎭 Scenario Impact", f"₹{scenario_impact:+,.2f}")
                    
                    # Cost per km analysis
                    distance = results.get('route_info', {}).get('distance_km', 1)
                    if distance > 0:
                        cost_per_km = best_price / distance
                        st.metric("📏 Cost per KM", f"₹{cost_per_km:.2f}")
                
            except Exception as e:
                st.warning(f"Cost breakdown unavailable: {e}")
                
            # Vendor recommendation insights
            st.markdown("### 🏆 Vendor Selection Insights")
            best_vendor = results.get('best_vendor', 'Unknown')
            vendors = results.get('all_vendors')
            
            if vendors is not None and not vendors.empty and best_vendor != 'Unknown':
                vendor_row = vendors[vendors['vendor'] == best_vendor]
                if not vendor_row.empty:
                    vendor_info = vendor_row.iloc[0]
                    
                    st.markdown(f"""
                    **Selected Vendor:** {best_vendor}
                    
                    **Key Strengths:**
                    - Cost Efficiency: ₹{vendor_info.get('cost_per_km', 0):.2f}/km
                    - Reliability Score: {vendor_info.get('reliability_score', 'N/A')}/10
                    - Delivery Speed: {vendor_info.get('delivery_speed', 'Standard')}
                    - Environmental Impact: {vendor_info.get('emission_per_km', 0):.2f} kg/km
                    """)
    
    with tab4:
        st.subheader("📋 Strategic Summary & Action Plan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Executive Summary")
            
            # Get strategic reasoning
            final_reasoning = results.get('crew_reasoning', 'Strategic analysis completed')
            
            # Create comprehensive summary
            route_info = results.get('route_info', {})
            risk_info = results.get('risk', {})
            
            summary_data = {
                'scenario': scenario_used,
                'route': f"{route_info.get('path', ['Unknown', 'Unknown'])[0]} → {route_info.get('path', ['Unknown', 'Unknown'])[1]}",
                'distance': f"{route_info.get('distance_km', 0):.0f} km",
                'duration': route_info.get('duration', 'Unknown'),
                'demand': f"{results.get('forecast', 0):,.0f} orders",
                'vendor': results.get('best_vendor', 'Unknown'),
                'cost': f"₹{results.get('best_price', 0):,.2f}",
                'risk_level': risk_info.get('risk_level', '🟡 Medium') if isinstance(risk_info, dict) else '🟡 Medium'
            }
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <h3>🎬 Scenario: {summary_data['scenario']}</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div><b>🛣️ Route:</b> {summary_data['route']}</div>
                <div><b>📏 Distance:</b> {summary_data['distance']}</div>
                <div><b>⏱️ Duration:</b> {summary_data['duration']}</div>
                <div><b>📈 Demand:</b> {summary_data['demand']}</div>
                <div><b>🏆 Vendor:</b> {summary_data['vendor']}</div>
                <div><b>💰 Cost:</b> {summary_data['cost']}</div>
            </div>
            <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 6px;">
                <b>⚠️ Risk Assessment:</b> {summary_data['risk_level']}
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Strategic Insights
            st.markdown("### 🤖 AI Strategic Insights")
            st.markdown(f"""
            <div style="background: #0; padding: 1.5rem; border-radius: 0px; 
                        border-left: 0px solid #28a745; margin-bottom: 1rem;">
                {final_reasoning}
            </div>
            """, unsafe_allow_html=True)
            
            # Action items with priority
            st.markdown("### ✅ Priority Action Items")
            
            action_items = [
                {
                    "priority": "🔴 URGENT",
                    "action": f"Confirm booking with {summary_data['vendor']} within 2 hours",
                    "timeline": "Immediate"
                },
                {
                    "priority": "🟡 HIGH",
                    "action": f"Monitor weather and traffic conditions for {summary_data['route'].split(' → ')[1]}",
                    "timeline": "Daily until delivery"
                },
                {
                    "priority": "🟡 HIGH", 
                    "action": f"Prepare inventory for {summary_data['demand']} demand spike",
                    "timeline": "Within 24 hours"
                },
                {
                    "priority": "🟢 MEDIUM",
                    "action": "Setup delivery tracking dashboard and notifications",
                    "timeline": "Before shipment"
                },
                {
                    "priority": "🟢 MEDIUM",
                    "action": "Review performance metrics post-delivery for optimization",
                    "timeline": "Post-delivery"
                }
            ]
            
            for i, item in enumerate(action_items, 1):
                st.markdown(f"""
                <div style="background:0; padding: 1rem; border-radius: 8px; 
                            border: 1px solid #e9ecef; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: between; align-items: center;">
                        <div style="flex: 1;">
                            <b>{i}. {item['action']}</b>
                        </div>
                        <div style="text-align: right; font-size: 0.8em;">
                            <div>{item['priority']}</div>
                            <div>⏰ {item['timeline']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Performance Metrics")
            
            # System performance indicators
            confidence_score = 85  # You can calculate this based on agent success rates
            efficiency_score = min(100, 120 - (results.get('best_price', 5000) / 100))
            sustainability_score = 70  # Based on vendor selection
            risk_score = 90 if '🟢' in str(risk_info.get('risk_level', '')) else 70 if '🟡' in str(risk_info.get('risk_level', '')) else 40
            
            metrics = {
                "🎯 Decision Confidence": f"{confidence_score}%",
                "⚡ Cost Efficiency": f"{efficiency_score:.0f}%", 
                "🌱 Sustainability Score": f"{sustainability_score}%",
                "🛡️ Risk Mitigation": f"{risk_score}%",
                "📈 Overall Performance": f"{(confidence_score + efficiency_score + sustainability_score + risk_score) / 4:.0f}%"
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
            
            # Export functionality
            st.markdown("### 📤 Export & Reports")
            
            # Prepare export data
            export_data = {
                "analysis_timestamp": execution_time.isoformat(),
                "scenario": scenario_used,
                "route_analysis": summary_data,
                "cost_breakdown": {
                    "selected_vendor": results.get('best_vendor'),
                    "total_cost": results.get('best_price'),
                    "cost_per_km": results.get('best_price', 0) / max(1, route_info.get('distance_km', 1))
                },
                "risk_assessment": risk_info,
                "strategic_recommendations": final_reasoning,
                "performance_metrics": metrics
            }
            
            # JSON export
            json_data = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                "📄 Download Executive Report (JSON)",
                json_data,
                file_name=f"supply_chain_analysis_{execution_time.strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            # CSV export for vendor data
            vendors = results.get("all_vendors")
            if vendors is not None and not vendors.empty:
                csv_data = vendors.to_csv(index=False)
                st.download_button(
                    "📊 Download Vendor Analysis (CSV)",
                    csv_data,
                    file_name=f"vendor_comparison_{execution_time.strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Enhanced Footer
st.markdown("---")
st.markdown("### 🏢 System Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #0; padding: 1rem; border-radius: 8px;">
    <h4>🤖 AI Multi-Agent System</h4>
    <ul style="margin: 0; padding-left: 1rem;">
    <li>5 Specialized AI Agents</li>
    <li>CrewAI Orchestration</li>
    <li>Real-time Decision Making</li>
    <li>Scenario-based Analysis</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #0; padding: 1rem; border-radius: 8px;">
    <h4>🔧 Integration & APIs</h4>
    <ul style="margin: 0; padding-left: 1rem;">
    <li>OpenAI GPT-4 Reasoning</li>
    <li>Google Maps Navigation</li>
    <li>WeatherAPI Monitoring</li>
    <li>Dynamic Route Optimization</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #0; padding: 1rem; border-radius: 8px;">
    <h4>📊 Key Capabilities</h4>
    <ul style="margin: 0; padding-left: 1rem;">
    <li>ARIMA Demand Forecasting</li>
    <li>Multi-Vendor Cost Analysis</li>
    <li>Weather Risk Assessment</li>
    <li>Strategic Recommendations</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #0; border-radius: 8px;">
    <p style="margin: 0; color: #6c757d;">
        🚀 <b>AI Supply Chain Optimizer</b> • Built with ❤️ using Multi-Agent Systems
    </p>
    <p style="margin: 0; color: #6c757d; font-size: 0.9em;">
        <em>Powered by CrewAI • Streamlit • OpenAI GPT-4 • Google Maps API • WeatherAPI</em>
    </p>
</div>
""", unsafe_allow_html=True)
