# 🇱🇰 Sri Lankan Economy Analyzer

An interactive web dashboard for analyzing Sri Lanka's economic indicators using World Bank data.

## 📊 Features

- **Economic Data Visualization**: Interactive charts showing reserves, inflation, and debt trends
- **Cross-Correlation Analysis**: Analyze relationships between economic indicators with lag analysis
- **Crisis Detection**: Identify economic crisis points and timelines
- **Signal Lab**: Advanced correlation analysis between variables

## 🚀 Live Dashboard

Access the live dashboard at: [Your Render URL]

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/sri-lankan-economy-analyzer.git
cd sri-lankan-economy-analyzer
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the main analysis:
```bash
python main.py
```

5. Run the dashboard:
```bash
cd src
python dashboard/app.py
```

## 📁 Project Structure

```
├── main.py                 # Main analysis pipeline
├── requirements.txt        # Python dependencies
├── src/
│   ├── dashboard/          # Dash web application
│   ├── ingestion/          # Data collection modules
│   ├── processing/         # Data cleaning & processing
│   └── models/             # Analysis models
├── data/
│   └── processed/          # Cleaned datasets
└── test_*.py              # Test files
```

## 📈 Data Sources

- **World Bank API**: Economic indicators (reserves, inflation, debt)
- **Time Period**: 2000-2024 (monthly frequency after processing)

## 🔬 Analysis Features

- **Cross-correlation**: Lag analysis between economic variables
- **Anomaly detection**: Statistical outlier identification
- **Crisis detection**: Economic crisis point identification
- **Time series processing**: Annual to monthly data conversion

## 🤝 Contributing

Feel free to contribute by:
- Adding more economic indicators
- Improving visualizations
- Adding new analysis features
- Enhancing the dashboard UI

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- World Bank for providing economic data
- Dash/Plotly for the web framework
- Open source Python community
