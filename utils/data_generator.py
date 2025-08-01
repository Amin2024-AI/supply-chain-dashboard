import pandas as pd
import numpy as np

def generate_data():
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    n_samples = len(dates)
    
    np.random.seed(42)
    data = {
        'date': dates,
        'delivery_time': np.random.normal(24, 5, n_samples),
        'vendor_performance': np.random.uniform(60, 100, n_samples),
        'defect_rate': np.random.uniform(1, 10, n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples)
    }
    return pd.DataFrame(data)
