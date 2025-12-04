import streamlit as st
import json
from streamlit_lottie import st_lottie
from style_utils import load_global_css

# --- PAGE CONFIG ---
# This MUST be the first command
st.set_page_config(
    page_title="EVision",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_global_css()

def load_lottie_local(filepath: str):
    """ Loads a Lottie file from a local path. """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: Could not find Lottie file at {filepath}")
        return None
    except json.JSONDecodeError:
        st.error("Error: Could not decode Lottie JSON file. Is it corrupted?")
        return None

lottie_hero_path = "assets/hero_lottie.json" # <-- New path
lottie_json = load_lottie_local(lottie_hero_path)

# --- HERO SECTION ---
col_hero_1, col_hero_2 = st.columns([2, 1.5], gap="large")

with col_hero_1:
    st.title("🔋⚡ EVision")
    st.markdown("### A unified dashboard for EV routing and infrastructure analysis.")
    st.markdown(f"<div style='color: #777; font-size: 1.1rem; animation: slideUp 0.8s ease-out;'>Project by Mrudul Rajgire, Nupur Kirwai, Chintamani Chaudhari</div>", unsafe_allow_html=True)
    
with col_hero_2:
    if lottie_json:
        st_lottie(lottie_json, speed=1, reverse=False, loop=True, quality="high", height=300, key="hero_lottie")
    else:
        st.error("Could not load animation.")

st.markdown("<hr style='animation-delay: 0.1s; animation-fill-mode: backwards;'>", unsafe_allow_html=True)
st.header("Please select an application to launch:")

# --- CARD TEMPLATES ---
CARD_TEMPLATE = """
<a href="{url}" target="_self" class="card-link">
    <div class="card">
        <p class="card-header">{icon} {title}</p>
        <p class="card-text">{text}</p>
    </div>
</a>
"""

card1_text = """
Plan your long-distance EV journey with perfect peace of mind.
<ul>
    <li>Calculates your route based on your EV's range.</li>
    <li>Finds charging stops automatically.</li>
    <li>Suggests points of interest (restaurants, cafes) while you charge.</li>
</ul>
"""

card2_text = """
Analyze and optimize EV charging infrastructure for smart cities.
<ul>
    <li>Identifies 'hot cities' with high EV station density.</li>
    <li>Uses K-Means clustering to find optimal new station locations.</li>
    <li>Provides a data-driven approach to infrastructure planning.</li>
</ul>
"""

# --- RENDER CARDS ---
col_card_1, col_card_2 = st.columns(2, gap="large")

with col_card_1:
    st.markdown(f"<div class='card-col-1'>{CARD_TEMPLATE.format(url='EV_Trip_Planner', icon='🚗', title='EV Trip Planner', text=card1_text)}</div>", unsafe_allow_html=True)

with col_card_2:
    st.markdown(f"<div class='card-col-2'>{CARD_TEMPLATE.format(url='Infra_Management', icon='📊', title='EV Infra Management', text=card2_text)}</div>", unsafe_allow_html=True)