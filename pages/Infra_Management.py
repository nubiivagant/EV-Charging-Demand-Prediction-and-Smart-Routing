import streamlit as st
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from preprocessing.preprocess import scale_coordinates
from visualization.plots import plot_clusters
from sklearn.metrics import silhouette_score
from style_utils import load_global_css

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EVision | Infra Management", # <-- Custom title
    page_icon="📊",
    layout="wide"
)

# --- LOAD GLOBAL CSS ---
load_global_css() 

# --- CUSTOM BACK BUTTON ---
st.markdown('<a href="/" target="_self" class="back-button">🏠 Back to Home</a>', unsafe_allow_html=True)

# --- PAGE CONTENT ---
st.title("📊 EV Infrastructure Management")
st.markdown("Analyze and optimize EV charging infrastructure using clustering.")
st.markdown("<hr>", unsafe_allow_html=True)

# --- Upload File ---
st.sidebar.header("⚙️ Data Source")
file_path = r"C:\Users\HP\Documents\EV_Project_Dashboard\EV_Project_Dashboard\data\ev_stations.xlsx"

try:
    df = pd.read_excel(file_path, sheet_name='ev_locations')
    #st.sidebar.info(f"Loaded data from: `{file_path}`")
except FileNotFoundError:
    st.error(f"❌ Error: File not found at `{file_path}`.")
    st.info("Please update the `file_path` variable in `app.py` (line 30) to the correct location of your Excel file.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while reading the file: {e}")
    st.stop()

# --- Data Cleaning ---
if not {'latitude', 'longitude', 'city'}.issubset(df.columns):
    st.error("The file must contain 'latitude', 'longitude', and 'city' columns.")
    st.stop()

df = df[['latitude', 'longitude', 'city', 'name']].dropna()

# --- Hot City Detection ---
st.sidebar.header("📍 City Selection")
city_counts = df['city'].value_counts()
hot_cities = city_counts[city_counts >= 10].index.tolist()

if not hot_cities:
    st.error("❌ No cities with enough EV stations (≥10) found.")
    st.stop()

selected_city = st.sidebar.selectbox("Select a Hot City", sorted(hot_cities))
city_df = df[df['city'] == selected_city]

if len(city_df) < 3:
    st.warning(f"{selected_city} has too few stations to cluster.")
    st.stop()

# --- Cluster Count Selection ---
max_clusters = min(10, len(city_df))
k = st.sidebar.slider("Number of Clusters", 2, max_clusters, 3)

# --- USE A SPINNER FOR CLUSTERING ---
with st.spinner(f"Analyzing {selected_city}..."):
    scaled_data, scaler = scale_coordinates(city_df)
    kmeans = KMeans(n_clusters=k, random_state=42)
    city_df['Cluster'] = kmeans.fit_predict(scaled_data)
    
    st.success(f"Analysis complete for {selected_city}!")

# --- Output ---
st.subheader(f"📊 Clusters in **{selected_city}** (K={k})")

# --- Map View ---
st.map(city_df[['latitude', 'longitude']])

# --- Cluster Plot ---
fig = plot_clusters(city_df, k)
st.pyplot(fig)

# --- Data View ---
with st.expander("📄 View Clustered Station Data"):
    st.dataframe(city_df)
    
# After predicting clusters
score = silhouette_score(scaled_data, city_df['Cluster'])
st.success(f"🧠 Silhouette Score: {score:.3f}")

# --- Footer ---
st.markdown("---")
st.markdown("Made to improve EV infrastructure planning.")
