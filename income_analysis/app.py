import streamlit as st
import pandas as pd
import numpy as np
import os

# Try to import plotly with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    st.error("Plotly is not installed. Please install it with: pip install plotly")
    PLOTLY_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="German Household Income Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def load_and_process_data():
    """Load and process the household income data from the CSV format"""
    try:
        # Get the path to the CSV file in the same directory
        csv_path = os.path.join(os.path.dirname(__file__), '12241-0001_en.csv')
        
        # Read the file line by line and parse manually
        data_rows = []
        current_year = None
        current_household_type = None
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        # Skip the first 7 lines (headers) and process data
        for i, line in enumerate(lines[7:], start=7):
            line = line.strip()
            if not line or line == '__________':
                continue
                
            # Split by semicolon
            parts = line.split(';')
            if len(parts) >= 8:
                year = parts[0].strip()
                household_type = parts[1].strip()
                household_count = parts[2].strip()
                count_flag = parts[3].strip()
                gross_income = parts[4].strip()
                gross_flag = parts[5].strip()
                net_income = parts[6].strip()
                net_flag = parts[7].strip()
                
                # Update current year if we have a new year
                if year and year.isdigit():
                    current_year = int(year)
                
                # Update current household type if we have one
                if household_type:
                    current_household_type = household_type
                
                # Only process rows that have a year (not empty)
                if current_year and current_household_type:
                    data_rows.append({
                        'year': current_year,
                        'household_type': current_household_type,
                        'household_count': household_count,
                        'count_flag': count_flag,
                        'gross_income': gross_income,
                        'net_income': net_income,
                        'gross_flag': gross_flag,
                        'net_flag': net_flag
                    })
        
        # Convert to DataFrame
        df = pd.DataFrame(data_rows)
        
        if len(df) == 0:
            st.error("No data found in CSV file!")
            return None, None
        
        # Clean household type names
        df['household_type_clean'] = df['household_type'].astype(str).str.strip()
        
        # Map household types to consistent English names
        household_mapping = {
            'Households without children': 'Households without children',
            'Persons living alone': 'Single person',
            'Two adults without children': 'Two adults without children',
            'Three or more adults without children': 'Three+ adults without children',
            'Households with children': 'Households with children',
            'Lone parents': 'Single parents',
            'Two adults with children': 'Two adults with children',
            'Three or more adults with children': 'Three+ adults with children',
            'Total': 'Total'
        }
        
        df['household_type_english'] = df['household_type_clean'].map(household_mapping)
        
        # Handle any unmapped household types by keeping them as-is
        df['household_type_english'] = df['household_type_english'].fillna(df['household_type_clean'])
        
        # Convert income columns to numeric
        df['gross'] = pd.to_numeric(df['gross_income'], errors='coerce')
        df['net'] = pd.to_numeric(df['net_income'], errors='coerce')
        
        # Remove rows where we don't have both gross and net income
        df = df.dropna(subset=['gross', 'net'])
        
        # Calculate tax rate
        df['tax_rate'] = ((df['gross'] - df['net']) / df['gross'] * 100).round(1)
        
        # Select only the columns we need
        result_data = df[['year', 'household_type_english', 'gross', 'net', 'tax_rate']].copy()
        
        return result_data, df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.write(f"Please make sure the CSV file is in the correct location: {csv_path}")
        return None, None

def create_income_comparison_chart(data, selected_households, selected_years):
    """Create gross vs net income comparison chart"""
    if not PLOTLY_AVAILABLE:
        st.error("Plotly is not available. Please install it to view charts.")
        return None
        
    filtered_data = data[
        (data['household_type_english'].isin(selected_households)) &
        (data['year'].isin(selected_years))
    ].copy()
    
    # Melt data for easier plotting
    chart_data = filtered_data.melt(
        id_vars=['year', 'household_type_english'],
        value_vars=['gross', 'net'],
        var_name='income_type',
        value_name='amount'
    )
    
    fig = px.line(
        chart_data,
        x='year',
        y='amount',
        color='household_type_english',
        line_dash='income_type',
        title='Gross vs Net Income by Household Type and Year',
        labels={
            'amount': 'Income (EUR/year)',
            'year': 'Year',
            'household_type_english': 'Household Type'
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        height=600,
        xaxis_title="Year",
        yaxis_title="Income (EUR/year)",
        legend_title="Household Type & Income Type",
        hovermode='x unified'
    )
    
    return fig

def create_tax_rate_chart(data, selected_households, selected_years):
    """Create tax rate comparison chart"""
    if not PLOTLY_AVAILABLE:
        st.error("Plotly is not available. Please install it to view charts.")
        return None
        
    filtered_data = data[
        (data['household_type_english'].isin(selected_households)) &
        (data['year'].isin(selected_years))
    ].copy()
    
    fig = px.bar(
        filtered_data,
        x='year',
        y='tax_rate',
        color='household_type_english',
        title='Effective Tax Rate by Household Type and Year',
        labels={
            'tax_rate': 'Tax Rate (%)',
            'year': 'Year',
            'household_type_english': 'Household Type'
        },
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Year",
        yaxis_title="Tax Rate (%)",
        legend_title="Household Type",
        hovermode='x unified'
    )
    
    return fig

def create_income_gap_chart(data, selected_households, selected_years):
    """Create income gap (gross - net) chart"""
    if not PLOTLY_AVAILABLE:
        st.error("Plotly is not available. Please install it to view charts.")
        return None
        
    filtered_data = data[
        (data['household_type_english'].isin(selected_households)) &
        (data['year'].isin(selected_years))
    ].copy()
    
    filtered_data['income_gap'] = filtered_data['gross'] - filtered_data['net']
    
    fig = px.bar(
        filtered_data,
        x='year',
        y='income_gap',
        color='household_type_english',
        title='Income Gap (Gross - Net) by Household Type and Year',
        labels={
            'income_gap': 'Income Gap (EUR/year)',
            'year': 'Year',
            'household_type_english': 'Household Type'
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Year",
        yaxis_title="Income Gap (EUR/year)",
        legend_title="Household Type",
        hovermode='x unified'
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🇩🇪 German Household Income Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check if plotly is available
    if not PLOTLY_AVAILABLE:
        st.warning("⚠️ Plotly is not installed. Charts will not be displayed. Please install with: pip install plotly")
    
    # Load data
    with st.spinner('Loading data...'):
        data, raw_data = load_and_process_data()
    
    if data is None or len(data) == 0:
        st.error("Failed to load data. Please check the CSV file.")
        return
    
    # Sidebar filters
    st.sidebar.header("📊 Filter Options")
    
    # Year filter
    available_years = sorted(data['year'].unique())
    selected_years = st.sidebar.multiselect(
        "Select Years:",
        options=available_years,
        default=available_years,
        help="Choose which years to include in the analysis"
    )
    
    # Household type filter
    available_households = sorted(data['household_type_english'].unique())
    selected_households = st.sidebar.multiselect(
        "Select Household Types:",
        options=available_households,
        default=available_households,
        help="Choose which household types to include in the analysis"
    )
    
    # Chart type selector
    chart_type = st.sidebar.selectbox(
        "Select Chart Type:",
        ["Income Comparison", "Tax Rate Analysis", "Income Gap Analysis", "All Charts"],
        help="Choose the type of analysis to display"
    )
    
    # Data summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Data Summary")
    total_records = len(data)
    years_covered = len(available_years)
    household_types = len(available_households)
    
    st.sidebar.metric("Total Records", f"{total_records:,}")
    st.sidebar.metric("Years Covered", years_covered)
    st.sidebar.metric("Household Types", household_types)
    
    # Main content
    if not selected_years or not selected_households:
        st.warning("⚠️ Please select at least one year and one household type to view the charts.")
        return
    
    # Filter data based on selections
    filtered_data = data[
        (data['year'].isin(selected_years)) &
        (data['household_type_english'].isin(selected_households))
    ]
    
    # Key metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_gross = filtered_data['gross'].mean()
        st.metric("Average Gross Income", f"€{avg_gross:,.0f}")
    
    with col2:
        avg_net = filtered_data['net'].mean()
        st.metric("Average Net Income", f"€{avg_net:,.0f}")
    
    with col3:
        avg_tax_rate = filtered_data['tax_rate'].mean()
        st.metric("Average Tax Rate", f"{avg_tax_rate:.1f}%")
    
    with col4:
        income_gap = avg_gross - avg_net
        st.metric("Average Income Gap", f"€{income_gap:,.0f}")
    
    st.markdown("---")
    
    # Charts section
    if chart_type == "Income Comparison" or chart_type == "All Charts":
        st.subheader("💰 Gross vs Net Income Comparison")
        income_chart = create_income_comparison_chart(data, selected_households, selected_years)
        if income_chart:
            st.plotly_chart(income_chart, width='stretch')
    
    if chart_type == "Tax Rate Analysis" or chart_type == "All Charts":
        st.subheader("📈 Effective Tax Rate Analysis")
        tax_chart = create_tax_rate_chart(data, selected_households, selected_years)
        if tax_chart:
            st.plotly_chart(tax_chart, width='stretch')
    
    if chart_type == "Income Gap Analysis" or chart_type == "All Charts":
        st.subheader("📉 Income Gap Analysis")
        gap_chart = create_income_gap_chart(data, selected_households, selected_years)
        if gap_chart:
            st.plotly_chart(gap_chart, width='stretch')
    
    # Data table
    st.markdown("---")
    st.subheader("📋 Detailed Data Table")
    
    # Display options
    col1, col2 = st.columns([1, 3])
    with col1:
        show_data = st.checkbox("Show detailed data table", value=False)
    
    if show_data:
        # Format the data for display
        display_data = filtered_data.copy()
        display_data['gross'] = display_data['gross'].round(0).astype(int)
        display_data['net'] = display_data['net'].round(0).astype(int)
        display_data['tax_rate'] = display_data['tax_rate'].round(1)
        
        # Rename columns for better display
        display_data = display_data.rename(columns={
            'year': 'Year',
            'household_type_english': 'Household Type',
            'gross': 'Gross Income (€)',
            'net': 'Net Income (€)',
            'tax_rate': 'Tax Rate (%)'
        })
        
        st.dataframe(display_data, width='stretch')
        
        # Download button
        csv = display_data.to_csv(index=False)
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name=f"german_household_income_{min(selected_years)}_{max(selected_years)}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
