# 🚀 AI Multi-Agent Supply Chain Optimizer

A comprehensive supply chain optimization platform powered by multi-agent AI systems, providing real-time decision-making capabilities for logistics operations across Indian cities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.36+-red.svg)
![CrewAI](https://img.shields.io/badge/crewai-0.60+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Key Features

### 🤖 Multi-Agent AI System
- **Demand Forecast Agent**: ARIMA-based demand prediction with scenario modeling
- **Route Optimizer Agent**: Google Maps integration with intelligent fallbacks
- **Cost Analyzer Agent**: Multi-vendor comparison with sustainability metrics
- **Risk Monitor Agent**: Weather-based risk assessment and mitigation
- **Strategic Coordinator**: AI-powered decision synthesis and recommendations

### 🧠 Advanced AI Integration
- **CrewAI Orchestration**: Coordinated multi-agent reasoning and decision-making
- **OpenAI GPT-4**: Strategic analysis and executive-level recommendations
- **Vector Database**: Route intelligence and historical performance learning
- **Scenario Modeling**: Dynamic operational scenario simulation

### 📊 Interactive Dashboard
- **Real-time Analytics**: Live agent execution monitoring and performance tracking
- **Route Visualization**: Interactive maps with optimized delivery paths
- **Cost Analysis**: Comprehensive vendor comparison and sustainability scoring
- **Executive Reports**: Downloadable strategic summaries and action plans

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Streamlit UI      │    │   Orchestrator      │    │   CrewAI Agents     │
│   - Dashboard       │◄──►│   - Coordination    │◄──►│   - Strategic AI    │
│   - Visualization   │    │   - Error Handling  │    │   - Reasoning       │
│   - User Interface  │    │   - Fallback Logic  │    │   - Recommendations │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                          │                          │
           ▼                          ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  Computational      │    │   Vector Database   │    │   External APIs     │
│  Agents             │    │   - Route History   │    │   - Google Maps     │
│  - Demand Forecast  │    │   - Performance     │    │   - Weather API     │
│  - Route Optimizer  │    │   - Intelligence    │    │   - OpenAI          │
│  - Cost Analyzer    │    │   - Learning        │    │   - Hugging Face    │
│  - Risk Monitor     │    └─────────────────────┘    └─────────────────────┘
└─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Optional: API keys for enhanced functionality

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-supply-chain-optimizer.git
   cd ai-supply-chain-optimizer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys (optional)
   ```

5. **Create data directory and files**
   ```bash
   mkdir -p data
   # Sample data files will be created automatically
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required for full AI functionality
OPENAI_API_KEY=your_openai_api_key

# Optional - enhances route optimization
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Optional - enables weather risk assessment
WEATHER_API_KEY=your_weather_api_key

# Optional - provides backup AI models
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### API Key Setup

1. **OpenAI API**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Google Maps API**: Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
3. **Weather API**: Get from [WeatherAPI.com](https://www.weatherapi.com/)
4. **Hugging Face**: Get from [Hugging Face Settings](https://huggingface.co/settings/tokens)

**Note**: The application works in fallback mode without API keys but provides enhanced functionality with proper configuration.

## 📁 Project Structure

```
ai-supply-chain-optimizer/
├── 📁 agents/                     # Computational agent implementations
│   ├── __init__.py
│   ├── demand_forecast_agent.py   # ARIMA demand forecasting
│   ├── route_optimizer_agent.py   # Route optimization with Google Maps
│   ├── cost_analyzer_agent.py     # Vendor cost analysis
│   └── risk_monitor_agent.py      # Weather risk assessment
├── 📁 data/                       # Data files
│   ├── orders.csv                 # Historical orders data
│   └── vendors.csv                # Vendor database
├── 📁 utils/                      # Utility modules
│   ├── __init__.py
│   ├── config.py                  # Configuration management
│   └── vector_db.py               # Vector database for route intelligence
├── 📄 app.py                     # Main Streamlit application
├── 📄 orchestrator.py            # Multi-agent orchestration
├── 📄 crew_setup.py              # CrewAI configuration
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env.example               # Environment variables template
└── 📄 README.md                  # Project documentation
```

## 🎬 Operational Scenarios

The system supports multiple operational scenarios with dynamic adjustments:

- **🟢 Normal Operations**: Baseline performance metrics
- **📈 Peak Season Demand (+40%)**: Holiday/festival surge handling
- **💰 Fuel Price Surge (+25%)**: Transportation cost impact analysis
- **🌪️ Monsoon Disruption**: Weather-related delay management
- **⚡ Emergency Supply**: Urgent delivery requirements
- **🏭 Industrial Strike**: Labor disruption impact assessment

## 📊 Key Capabilities

### Demand Forecasting
- ARIMA time series modeling
- Seasonal pattern recognition
- Scenario-based adjustments
- Confidence scoring

### Route Optimization
- Google Maps API integration
- Real-time traffic consideration
- Historical route intelligence
- Multiple optimization criteria (cost, time, efficiency)

### Cost Analysis
- Multi-vendor comparison
- Sustainability metrics
- Total cost of ownership
- Risk-adjusted pricing

### Risk Assessment
- Weather impact analysis
- Operational risk scoring
- Mitigation strategy recommendations
- Contingency planning

### AI-Powered Insights
- Strategic decision synthesis
- Executive-level recommendations
- Performance optimization
- Continuous learning

## 🔍 Usage Examples

### Basic Analysis
```python
from orchestrator import Orchestrator

# Initialize orchestrator
orchestrator = Orchestrator()

# Run comprehensive analysis
results = orchestrator.run_comprehensive_analysis(
    orders_csv="data/orders.csv",
    origin="Mumbai",
    destination="Delhi",
    scenario="🟢 Normal Operations"
)

print(f"Best vendor: {results['best_vendor']}")
print(f"Total cost: ₹{results['best_price']:,.2f}")
print(f"Risk level: {results['risk']['risk_level']}")
```

### Scenario Comparison
```python
scenarios = [
    "🟢 Normal Operations",
    "📈 Peak Season Demand (+40%)",
    "🌪️ Monsoon Disruption"
]

for scenario in scenarios:
    results = orchestrator.run_comprehensive_analysis(
        origin="Mumbai",
        destination="Bangalore", 
        scenario=scenario
    )
    print(f"{scenario}: ₹{results['best_price']:,.2f}")
```

## 🛡️ Error Handling & Fallbacks

The system includes comprehensive error handling and fallback mechanisms:

### API Failures
- **Google Maps**: Falls back to distance matrix estimation
- **Weather API**: Uses seasonal/location-based intelligence
- **OpenAI**: Provides computational analysis framework

### Data Issues
- **Missing Data**: Automatically generates sample data
- **Invalid Inputs**: Input validation and sanitization
- **Corrupted Files**: Fallback to default configurations

### System Resilience
- **Graceful Degradation**: Partial functionality during outages
- **Retry Logic**: Automatic retry for transient failures
- **Comprehensive Logging**: Full execution trail for debugging

## 📈 Performance Metrics

### System Health Indicators
- **Agent Success Rate**: Individual agent performance tracking
- **Response Time**: Average execution time monitoring
- **API Availability**: Real-time API status checking
- **Confidence Score**: Decision reliability assessment

### Business Metrics
- **Cost Efficiency**: Optimization effectiveness measurement
- **Delivery Performance**: On-time delivery rate tracking
- **Customer Satisfaction**: Service quality monitoring
- **Sustainability Score**: Environmental impact assessment

## 🧪 Testing

### Unit Tests
```bash
# Run individual agent tests
python -m pytest tests/test_agents.py

# Run orchestrator tests
python -m pytest tests/test_orchestrator.py
```

### Integration Tests
```bash
# Test API integrations
python -m pytest tests/test_integrations.py

# Test end-to-end workflows
python -m pytest tests/test_e2e.py
```

### Performance Tests
```bash
# Load testing
python -m pytest tests/test_performance.py
```

## 🔮 Roadmap & Future Enhancements

### Short Term (Q2 2024)
- [ ] Mobile responsive dashboard
- [ ] Advanced cost optimization algorithms
- [ ] Real-time tracking integration
- [ ] Enhanced weather prediction models

### Medium Term (Q3-Q4 2024)
- [ ] Machine learning demand forecasting
- [ ] IoT device integration
- [ ] Blockchain supply chain verification
- [ ] Advanced analytics and reporting

### Long Term (2025)
- [ ] Autonomous vehicle integration
- [ ] Predictive maintenance capabilities
- [ ] Global supply chain expansion
- [ ] Sustainability optimization

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `pytest`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings for all functions
- Include unit tests for new features
- Update documentation as needed

## 📋 Troubleshooting

### Common Issues

**Installation Problems**
```bash
# If you get dependency conflicts
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**API Key Issues**
- Verify API keys are correctly set in `.env`
- Check API key permissions and quotas
- Test individual APIs independently

**Streamlit Issues**
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with verbose logging
streamlit run app.py --logger.level=debug
```

**Memory Issues**
- Reduce data size for testing
- Use pagination for large datasets
- Monitor system resources

### Getting Help

1. Check the [FAQ](docs/FAQ.md)
2. Search [existing issues](https://github.com/your-username/ai-supply-chain-optimizer/issues)
3. Create a [new issue](https://github.com/your-username/ai-supply-chain-optimizer/issues/new) with:
   - System information
   - Error messages
   - Steps to reproduce

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent AI framework
- **OpenAI**: GPT-4 language model
- **Streamlit**: Web application framework
- **Google Maps**: Route optimization API
- **WeatherAPI**: Weather data services

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/ai-supply-chain-optimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/ai-supply-chain-optimizer/discussions)
- **Email**: support@yourdomain.com

---

<div align="center">

**🚀 Built with ❤️ for the Future of Supply Chain Optimization**

[Demo](https://demo-link.com) • [Documentation](https://docs-link.com) • [Report Bug](https://github.com/your-username/ai-supply-chain-optimizer/issues) • [Request Feature](https://github.com/your-username/ai-supply-chain-optimizer/issues)

</div>