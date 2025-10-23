# German Household Income Analysis Dashboard

A comprehensive Streamlit dashboard for analyzing German household income data from the Federal Statistical Office.

## 📊 Features

- **Interactive Visualizations**: Gross vs Net income comparison, tax rate analysis, and income gap analysis
- **Flexible Filtering**: Filter by years (2020-2024) and household types
- **9 Household Categories**: 
  - Households without children
  - Single person
  - Two adults without children
  - Three+ adults without children
  - Households with children
  - Single parents
  - Two adults with children
  - Three+ adults with children
  - Total
- **Key Metrics**: Average gross/net income, tax rates, and income gaps
- **Data Export**: Download filtered data as CSV

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Deployment
The dashboard is ready for deployment on:
- Streamlit Cloud
- Heroku
- Docker
- AWS/Azure

## 📁 Project Structure
```
income_analysis/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── 12241-0001_en.csv        # German household income dataset
└── README.md                # This file
```

## 📈 Data Source
Data from the German Federal Statistical Office (Destatis) - EU-SILC survey on household income and living conditions.

## 🔧 Technical Details
- **Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Python Version**: 3.7+

## 📊 Dashboard Sections

1. **Key Metrics**: Overview statistics
2. **Income Comparison**: Gross vs Net income trends
3. **Tax Rate Analysis**: Effective tax rates by household type
4. **Income Gap Analysis**: Difference between gross and net income
5. **Data Table**: Detailed data view with export functionality

## 🎯 Usage
1. Select years and household types from the sidebar
2. Choose chart type or view all charts
3. Explore the interactive visualizations
4. Download filtered data as needed

## 📝 License
MIT License - see LICENSE file for details
