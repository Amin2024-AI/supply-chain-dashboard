import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Supply Chain Analytics", layout="wide")

# Data Generation
@st.cache_data
def generate_data():
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    n_samples = len(dates)
    
    data = {
        'date': dates,
        'delivery_time': np.random.normal(24, 5, n_samples),
        'vendor_performance': np.random.uniform(60, 100, n_samples),
        'defect_rate': np.random.uniform(1, 10, n_samples),
        'inventory_level': np.random.uniform(1000, 5000, n_samples),
        'shipping_cost': np.random.uniform(500, 2000, n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples)
    }
    return pd.DataFrame(data)

# Load data
df = generate_data()

# Sidebar filters
st.sidebar.header('Filters')
selected_regions = st.sidebar.multiselect('Select Regions', 
                                        df['region'].unique(), 
                                        default=df['region'].unique())

# Filter data
filtered_df = df[df['region'].isin(selected_regions)]

# Main dashboard
st.title('Supply Chain Analytics Dashboard')

# KPI Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Delivery Time", 
              f"{filtered_df['delivery_time'].mean():.1f}h",
              f"{filtered_df['delivery_time'].mean() - df['delivery_time'].mean():.1f}h")
with col2:
    st.metric("Vendor Performance", 
              f"{filtered_df['vendor_performance'].mean():.1f}%",
              f"{filtered_df['vendor_performance'].mean() - df['vendor_performance'].mean():.1f}%")
with col3:
    st.metric("Defect Rate", 
              f"{filtered_df['defect_rate'].mean():.1f}%",
              f"{filtered_df['defect_rate'].mean() - df['defect_rate'].mean():.1f}%")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    # Delivery Time Trends
    fig_delivery = px.line(filtered_df, 
                          x='date', 
                          y='delivery_time',
                          title='Delivery Time Trends')
    st.plotly_chart(fig_delivery, use_container_width=True)

with col2:
    # Regional Performance
    fig_regional = px.box(filtered_df, 
                         x='region', 
                         y='delivery_time',
                         title='Delivery Time by Region')
    st.plotly_chart(fig_regional, use_container_width=True)

# Data Table
st.header('Detailed Data View')
st.dataframe(filtered_df, height=300)

# Download Button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="supply_chain_data.csv",
    mime="text/csv"
)
