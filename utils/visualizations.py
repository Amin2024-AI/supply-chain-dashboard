import plotly.express as px

def create_delivery_trend(df):
    fig = px.line(df, 
                  x='date', 
                  y='delivery_time', 
                  title='Delivery Time Trends')
    return fig

def create_regional_box(df):
    fig = px.box(df, 
                 x='region', 
                 y='delivery_time', 
                 title='Delivery Time by Region')
    return fig
