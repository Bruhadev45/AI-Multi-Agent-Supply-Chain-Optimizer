# alert_system.py
"""
Real-Time Alert System for AI Supply Chain Optimizer
This module provides proactive monitoring and actionable alerts
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Tuple, Any
import logging
import requests
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================================
# ALERT TYPES AND PRIORITIES
# ============================================================================

class AlertPriority(Enum):
    CRITICAL = "🔴 CRITICAL"
    HIGH = "🟠 HIGH"
    MEDIUM = "🟡 MEDIUM"
    LOW = "🟢 LOW"
    INFO = "🔵 INFO"

class AlertType(Enum):
    WEATHER = "Weather Risk"
    DEMAND_SPIKE = "Demand Spike"
    VENDOR_DEAL = "Vendor Opportunity"
    CAPACITY = "Capacity Warning"
    ROUTE = "Route Optimization"
    INVENTORY = "Inventory Alert"
    COST = "Cost Saving"
    RISK = "Risk Detection"

@dataclass
class Alert:
    """Structure for system alerts"""
    timestamp: datetime
    priority: AlertPriority
    alert_type: AlertType
    title: str
    message: str
    action_required: str
    impact: str
    data: Dict[str, Any]

# ============================================================================
# REAL-TIME MONITORING ENGINE
# ============================================================================

class RealTimeMonitor:
    """Continuously monitors supply chain metrics and generates alerts"""
    
    def __init__(self, agents=None):
        self.agents = agents
        self.alerts: List[Alert] = []
        self.monitoring_active = False
        self.check_interval = 60  # Check every 60 seconds
        self.last_check = datetime.now()
        
        # Thresholds for alerts
        self.thresholds = {
            'demand_spike': 1.3,  # 30% above normal
            'capacity_critical': 0.9,  # 90% capacity
            'weather_risk': 0.7,  # 70% chance of disruption
            'cost_variance': 0.15,  # 15% cost difference
            'inventory_low': 0.2,  # 20% of normal stock
        }
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        self.monitoring_active = True
        logger.info("Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        logger.info("Real-time monitoring stopped")
    
    def check_all_conditions(self) -> List[Alert]:
        """Run all monitoring checks and return new alerts"""
        new_alerts = []
        current_time = datetime.now()
        
        # 1. Weather Monitoring
        weather_alerts = self._check_weather_conditions()
        new_alerts.extend(weather_alerts)
        
        # 2. Demand Monitoring
        demand_alerts = self._check_demand_patterns()
        new_alerts.extend(demand_alerts)
        
        # 3. Vendor Price Monitoring
        vendor_alerts = self._check_vendor_prices()
        new_alerts.extend(vendor_alerts)
        
        # 4. Capacity Monitoring
        capacity_alerts = self._check_capacity_levels()
        new_alerts.extend(capacity_alerts)
        
        # 5. Route Optimization Opportunities
        route_alerts = self._check_route_optimization()
        new_alerts.extend(route_alerts)
        
        # 6. Inventory Levels
        inventory_alerts = self._check_inventory_levels()
        new_alerts.extend(inventory_alerts)
        
        # Store alerts
        self.alerts.extend(new_alerts)
        self.last_check = current_time
        
        return new_alerts
    
    def _check_weather_conditions(self) -> List[Alert]:
        """Monitor weather for all active routes"""
        alerts = []
        
        # Simulate weather check for major cities
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
        
        for city in cities:
            # Simulate weather risk (in production, use real weather API)
            risk_score = np.random.random()
            
            if risk_score > 0.7:  # High risk threshold
                alert = Alert(
                    timestamp=datetime.now(),
                    priority=AlertPriority.HIGH,
                    alert_type=AlertType.WEATHER,
                    title=f"⛈️ Severe Weather Alert - {city}",
                    message=f"Heavy rainfall expected in {city} region in next 6 hours. "
                           f"Risk score: {risk_score:.0%}. Estimated 300+ packages affected.",
                    action_required=f"IMMEDIATE: Reroute {city} packages via alternate hub. "
                                   f"Consider Pune hub for Mumbai, Noida for Delhi.",
                    impact=f"Potential 4-6 hour delays for {np.random.randint(200, 500)} packages",
                    data={'city': city, 'risk_score': risk_score, 'affected_packages': np.random.randint(200, 500)}
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_demand_patterns(self) -> List[Alert]:
        """Monitor demand spikes and anomalies"""
        alerts = []
        
        # Simulate demand check
        current_demand = np.random.randint(800, 1500)
        average_demand = 1000
        spike_ratio = current_demand / average_demand
        
        if spike_ratio > self.thresholds['demand_spike']:
            alert = Alert(
                timestamp=datetime.now(),
                priority=AlertPriority.HIGH,
                alert_type=AlertType.DEMAND_SPIKE,
                title=f"📈 Demand Spike Detected",
                message=f"Current orders: {current_demand} ({spike_ratio:.0%} of normal). "
                       f"Expecting {current_demand * 24} orders in next 24 hours.",
                action_required=f"1. Book additional capacity NOW (need {int((spike_ratio - 1) * 10)} extra vehicles)\n"
                               f"2. Alert warehouse to prepare for {spike_ratio:.0%} higher volume\n"
                               f"3. Contact backup vendors for overflow",
                impact=f"Revenue opportunity: ₹{current_demand * 500:,} additional",
                data={'current_demand': current_demand, 'spike_ratio': spike_ratio}
            )
            alerts.append(alert)
        
        return alerts
    
    def _check_vendor_prices(self) -> List[Alert]:
        """Monitor vendor pricing for opportunities"""
        alerts = []
        
        # Simulate vendor price check
        vendors = [
            {'name': 'FastLog Express', 'route': 'Delhi-Mumbai', 'discount': 35, 'valid_hours': 24},
            {'name': 'QuickShip Pro', 'route': 'Bangalore-Chennai', 'discount': 20, 'valid_hours': 12},
            {'name': 'SwiftCargo', 'route': 'Kolkata-Delhi', 'discount': 40, 'valid_hours': 6},
        ]
        
        for vendor in vendors:
            if vendor['discount'] >= 30:
                alert = Alert(
                    timestamp=datetime.now(),
                    priority=AlertPriority.MEDIUM,
                    alert_type=AlertType.VENDOR_DEAL,
                    title=f"💰 Cost Saving Opportunity - {vendor['discount']}% OFF",
                    message=f"{vendor['name']} offering {vendor['discount']}% discount on {vendor['route']} route. "
                           f"Valid for next {vendor['valid_hours']} hours only.",
                    action_required=f"Book immediately for next week's {vendor['route']} shipments. "
                                   f"Potential savings: ₹{np.random.randint(50000, 200000):,}",
                    impact=f"Can reduce this route's cost by ₹{np.random.randint(50000, 200000):,}",
                    data=vendor
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_capacity_levels(self) -> List[Alert]:
        """Monitor capacity utilization"""
        alerts = []
        
        # Simulate capacity check
        current_capacity = np.random.uniform(0.7, 1.0)
        tomorrow_forecast = np.random.randint(1000, 1500)
        available_capacity = 1200
        
        if tomorrow_forecast / available_capacity > self.thresholds['capacity_critical']:
            shortage = tomorrow_forecast - available_capacity
            alert = Alert(
                timestamp=datetime.now(),
                priority=AlertPriority.CRITICAL,
                alert_type=AlertType.CAPACITY,
                title=f"🚨 Capacity Crisis Tomorrow",
                message=f"Tomorrow's demand ({tomorrow_forecast} orders) exceeds capacity ({available_capacity}). "
                       f"SHORT by {shortage} orders!",
                action_required=f"URGENT - Do ALL of these NOW:\n"
                               f"1. Book {int(shortage/100)} additional vehicles from Vendor B\n"
                               f"2. Negotiate overtime with current drivers\n"
                               f"3. Alert customers about possible delays\n"
                               f"4. Prioritize premium customers",
                impact=f"Without action: {shortage} delayed orders, ₹{shortage * 1000:,} in penalties",
                data={'forecast': tomorrow_forecast, 'capacity': available_capacity, 'shortage': shortage}
            )
            alerts.append(alert)
        
        return alerts
    
    def _check_route_optimization(self) -> List[Alert]:
        """Identify route optimization opportunities"""
        alerts = []
        
        # Simulate finding inefficient routes
        inefficient_routes = [
            {'from': 'Warehouse A', 'to': 'Sector 15', 'current_distance': 45, 'optimal_distance': 32},
            {'from': 'Hub B', 'to': 'Industrial Area', 'current_distance': 38, 'optimal_distance': 28},
        ]
        
        for route in inefficient_routes:
            savings_percent = (1 - route['optimal_distance']/route['current_distance']) * 100
            if savings_percent > 20:
                alert = Alert(
                    timestamp=datetime.now(),
                    priority=AlertPriority.LOW,
                    alert_type=AlertType.ROUTE,
                    title=f"🗺️ Route Optimization Found",
                    message=f"Route {route['from']} → {route['to']} can be reduced from "
                           f"{route['current_distance']}km to {route['optimal_distance']}km",
                    action_required=f"Update driver app with new route. "
                                   f"Train drivers on new path via Highway 47 bypass",
                    impact=f"Save {savings_percent:.0f}% distance, ₹{np.random.randint(5000, 15000):,}/month in fuel",
                    data=route
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_inventory_levels(self) -> List[Alert]:
        """Monitor inventory levels for stockout risks"""
        alerts = []
        
        # Simulate inventory check
        products = [
            {'name': 'iPhone 15', 'current_stock': 45, 'daily_demand': 50, 'lead_time_days': 3},
            {'name': 'Samsung TV', 'current_stock': 20, 'daily_demand': 25, 'lead_time_days': 5},
        ]
        
        for product in products:
            days_of_stock = product['current_stock'] / product['daily_demand']
            if days_of_stock < product['lead_time_days']:
                alert = Alert(
                    timestamp=datetime.now(),
                    priority=AlertPriority.HIGH,
                    alert_type=AlertType.INVENTORY,
                    title=f"📦 Stockout Risk - {product['name']}",
                    message=f"Only {product['current_stock']} units left ({days_of_stock:.1f} days). "
                           f"Lead time is {product['lead_time_days']} days!",
                    action_required=f"ORDER NOW: Need {product['daily_demand'] * product['lead_time_days']} units. "
                                   f"Contact supplier immediately for express shipping",
                    impact=f"Stockout will lose ₹{product['daily_demand'] * 15000:,}/day in revenue",
                    data=product
                )
                alerts.append(alert)
        
        return alerts

# ============================================================================
# ALERT DASHBOARD UI
# ============================================================================

class AlertDashboard:
    """Streamlit UI for displaying real-time alerts"""
    
    def __init__(self):
        self.monitor = RealTimeMonitor()
    
    def render(self):
        """Render the alert dashboard in Streamlit"""
        st.title("🚨 Real-Time Supply Chain Command Center")
        
        # Control Panel
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🟢 Start Monitoring", type="primary"):
                self.monitor.start_monitoring()
                st.success("Monitoring activated!")
        with col2:
            if st.button("🔴 Stop Monitoring"):
                self.monitor.stop_monitoring()
                st.info("Monitoring paused")
        with col3:
            if st.button("🔄 Check Now"):
                self._run_checks()
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh (every 60 seconds)", value=True)
        
        # Alert Statistics
        st.markdown("---")
        self._show_statistics()
        
        # Active Alerts Section
        st.markdown("---")
        st.subheader("📢 Active Alerts - Action Required")
        
        # Get new alerts
        if st.session_state.get('last_check', 0) == 0 or \
           (datetime.now() - st.session_state.get('last_check_time', datetime.now())).seconds > 60:
            self._run_checks()
        
        # Display alerts by priority
        self._display_alerts()
        
        # Auto-refresh logic
        if auto_refresh:
            time.sleep(60)
            st.rerun()
    
    def _run_checks(self):
        """Run monitoring checks"""
        new_alerts = self.monitor.check_all_conditions()
        
        if 'all_alerts' not in st.session_state:
            st.session_state.all_alerts = []
        
        st.session_state.all_alerts.extend(new_alerts)
        st.session_state.last_check = len(new_alerts)
        st.session_state.last_check_time = datetime.now()
        
        # Show notification for new critical alerts
        critical_alerts = [a for a in new_alerts if a.priority == AlertPriority.CRITICAL]
        if critical_alerts:
            st.error(f"⚠️ {len(critical_alerts)} CRITICAL ALERTS REQUIRE IMMEDIATE ACTION!")
    
    def _show_statistics(self):
        """Show alert statistics"""
        col1, col2, col3, col4 = st.columns(4)
        
        alerts = st.session_state.get('all_alerts', [])
        
        with col1:
            st.metric("Total Alerts Today", len(alerts))
        with col2:
            critical = len([a for a in alerts if a.priority == AlertPriority.CRITICAL])
            st.metric("Critical Issues", critical, delta=critical)
        with col3:
            savings = sum([a.data.get('savings', 0) for a in alerts if a.alert_type == AlertType.VENDOR_DEAL])
            st.metric("Potential Savings", f"₹{savings:,.0f}")
        with col4:
            st.metric("Last Check", st.session_state.get('last_check_time', datetime.now()).strftime("%H:%M:%S"))
    
    def _display_alerts(self):
        """Display alerts grouped by priority"""
        alerts = st.session_state.get('all_alerts', [])
        
        if not alerts:
            st.info("✅ All systems operating normally. No alerts at this time.")
            return
        
        # Sort by priority and time
        priority_order = {
            AlertPriority.CRITICAL: 0,
            AlertPriority.HIGH: 1,
            AlertPriority.MEDIUM: 2,
            AlertPriority.LOW: 3,
            AlertPriority.INFO: 4
        }
        
        alerts.sort(key=lambda x: (priority_order[x.priority], -x.timestamp.timestamp()))
        
        # Display each alert
        for alert in alerts[:10]:  # Show latest 10 alerts
            self._render_alert_card(alert)
    
    def _render_alert_card(self, alert: Alert):
        """Render a single alert card"""
        # Choose container color based on priority
        if alert.priority == AlertPriority.CRITICAL:
            container = st.error
        elif alert.priority == AlertPriority.HIGH:
            container = st.warning
        elif alert.priority == AlertPriority.MEDIUM:
            container = st.info
        else:
            container = st.success
        
        with container(f"{alert.priority.value} | {alert.title}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Situation:** {alert.message}")
                st.write(f"**Action Required:** {alert.action_required}")
                st.write(f"**Business Impact:** {alert.impact}")
            
            with col2:
                st.write(f"**Time:** {alert.timestamp.strftime('%H:%M')}")
                st.write(f"**Type:** {alert.alert_type.value}")
                if st.button("✓ Acknowledge", key=f"ack_{alert.timestamp}"):
                    st.success("Alert acknowledged")

# ============================================================================
# INTEGRATION WITH EXISTING PROJECT
# ============================================================================

def integrate_with_orchestrator(orchestrator):
    """
    Integrate alert system with existing orchestrator
    
    Add this to your orchestrator.py:
    from alert_system import AlertDashboard, integrate_with_orchestrator
    """
    dashboard = AlertDashboard()
    dashboard.monitor.agents = orchestrator.agents
    return dashboard

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Standalone testing
    st.set_page_config(
        page_title="Supply Chain Command Center",
        page_icon="🚨",
        layout="wide"
    )
    
    dashboard = AlertDashboard()
    dashboard.render()