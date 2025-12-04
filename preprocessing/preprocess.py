import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(path):
    df = pd.read_excel(path, sheet_name='ev_locations')
    df = df[['latitude', 'longitude', 'name', 'city']].dropna()
    return df

def scale_coordinates(df):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[['latitude', 'longitude']])
    return scaled, scaler
