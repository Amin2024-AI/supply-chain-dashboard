import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration with minimal layout
st.set_page_config(page_title="Supply Chain Analytics", layout="wide", initial_sidebar_state="collapsed")

# Efficient data generation with longer cache duration
@st.cache_data(ttl=3600)  # Cache for 1 hour
def generate_data():
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')  # Reduced date range
    n_samples = len(dates)
    
    np.random.seed(42)  # Set seed for consistent data
    data = {
        'date': dates,
        'delivery_time': np.random.normal(24, 5, n_samples),
        'vendor_performance': np.random.uniform(60, 100, n_samples),
        'defect_rate': np.random.uniform(1, 10, n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples)
    }
    return pd.DataFrame(data)

# Load data once
df = generate_data()

# Sidebar with minimal filters
with st.sidebar:
    st.header('Filters')
    selected_regions = st.multiselect('Select Regions', 
                                    df['region'].unique(), 
                                    default=df['region'].unique())

# Filter data once and reuse
filtered_df = df[df['region'].isin(selected_regions)].copy()

# Main dashboard with optimized layout
st.title('Supply Chain Analytics Dashboard')

# KPI Metrics in a single row
metrics = st.columns(3)
with metrics[0]:
    st.metric("Avg Delivery Time", f"{filtered_df['delivery_time'].mean():.1f}h")
with metrics[1]:
    st.metric("Avg Vendor Performance", f"{filtered_df['vendor_performance'].mean():.1f}%")
with metrics[2]:
    st.metric("Avg Defect Rate", f"{filtered_df['defect_rate'].mean():.1f}%")

# Efficient visualizations
charts = st.columns(2)
with charts[0]:
    fig_delivery = px.line(filtered_df, 
                          x='date', 
                          y='delivery_time',
                          title='Delivery Time Trends')
    st.plotly_chart(fig_delivery, use_container_width=True)

with charts[1]:
    fig_regional = px.box(filtered_df, 
                         x='region', 
                         y='delivery_time',
                         title='Delivery Time by Region')
    st.plotly_chart(fig_regional, use_container_width=True)

# Efficient data table with pagination
st.header('Detailed Data View')
st.dataframe(filtered_df.head(1000), height=300)  # Limit rows for better performance

# Download functionality
if st.button('Download Data'):
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Click to Download",
        data=csv,
        file_name="supply_chain_data.csv",
        mime="text/csv"
    )
