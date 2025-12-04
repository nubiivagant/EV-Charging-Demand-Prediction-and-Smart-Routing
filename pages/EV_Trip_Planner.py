import streamlit as st
import requests
import polyline
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import time
import json
import uuid
from streamlit_lottie import st_lottie
from style_utils import load_global_css

# ------------- FUNCTIONS -------------
# (Your helper functions: get_coords, get_route, etc. remain unchanged)
def get_coords(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def get_route(start, end, ors_api_key):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ors_api_key, "Content-Type": "application/json"}
    body = {
        "coordinates": [[start[1], start[0]], [end[1], end[0]]],
        "instructions": False
    }
    res = requests.post(url, json=body, headers=headers)
    res.raise_for_status()
    data = res.json()
    geometry = polyline.decode(data['routes'][0]['geometry'])
    summary = data['routes'][0]['summary']  # contains distance (m) and duration (s)
    return geometry, summary

def get_mapmyindia_token(client_id, client_secret):
    token_url = "https://outpost.mapmyindia.com/api/security/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    res = requests.post(token_url, data=payload)
    return res.json().get("access_token")

def show_nearby_chargers(lat, lon, token):
    url = f"https://atlas.mapmyindia.com/api/places/nearby/json?keywords=ev+charging+station&refLocation={lat},{lon}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
    except:
        return [] # Return empty list on failure
    return data.get("suggestedLocations", [])

def get_poi(lat, lon, token, keyword):
    url = f"https://atlas.mapmyindia.com/api/places/nearby/json?keywords={keyword}&refLocation={lat},{lon}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    try:
        data = res.json()
        return data.get("suggestedLocations", [])
    except:
        return []

# ------------- STREAMLIT UI -------------
# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EVision | Trip Planner",
    page_icon="🚗",
    layout="wide"
)

# --- LOAD GLOBAL CSS ---
load_global_css()

# --- LOTTIE LOADER ---
@st.cache_data # Cache the lottie file
def load_lottie_local(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading Lottie file: {e}")
        return None

lottie_spinner_json = load_lottie_local("assets/spinner_lottie.json")

# --- CUSTOM BACK BUTTON ---
st.markdown('<a href="/" target="_self" class="back-button">🏠 Back to Home</a>', unsafe_allow_html=True)

# --- PAGE CONTENT ---
st.title("🚗 EV Trip Planner")
st.markdown("Plan your long-distance EV journey with perfect peace of mind.")
st.markdown("<hr>", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
# We use this to manage the state of the app
if 'trip_in_progress' not in st.session_state:
    st.session_state.trip_in_progress = False
if 'trip_results' not in st.session_state:
    st.session_state.trip_results = None

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("🔋 EV Specifications")
    battery_capacity = st.slider(
        "Battery Capacity (kWh)", 30, 100, 60, 5,
        help="Enter your EV's total battery capacity"
    )
    ev_range_km = st.slider(
        "EV Range (km)", 100, 500, 250, 10,
        help="Approximate full-charge driving range"
    )
    avg_speed = st.slider(
        "Average Speed (km/h)", 40, 120, 70, 5,
        help="Estimated average driving speed"
    )
    charger_power = 50  # kW

    st.header("📍 Route")
    start_city = st.text_input("Enter Start City", "Nagpur")
    end_city = st.text_input("Enter Destination City", "Pune")
    safe_limit_km = int(ev_range_km * 0.8)

    # --- PLAN TRIP BUTTON ---
    if st.button("Plan Trip", use_container_width=True):
        # 1. SET THE STATE TO "RUNNING"
        st.session_state.trip_in_progress = True
        st.session_state.trip_results = None # Clear old results
        st.rerun() 


# --- LOGIC & SPINNER BLOCK ---
# This block runs ONLY after the button is pressed and 'trip_in_progress' is True
if st.session_state.trip_in_progress:
    
    # 1. Create a placeholder for the spinner
    placeholder = st.empty()

    with placeholder.container():
        # 2. Show the Lottie animation
        if lottie_spinner_json:
            st_lottie(lottie_spinner_json, speed=1, loop=True, quality="high", height=150, width=150, key="lottie_spinner")
        else:
            st.warning("Could not load local spinner animation. Showing default spinner.")
            st.spinner("Finding the best route and charging stops...") # Fallback

    # 3. RUN ALL YOUR LOGIC (this will run while the Lottie is visible)
    start = get_coords(start_city)
    end = get_coords(end_city)
    
    if not all(start) or not all(end):
        st.error("Invalid city names")
        st.session_state.trip_in_progress = False # Stop running
        placeholder.empty() # Clear the spinner
        st.rerun() # Rerun to clear the error on next interaction
        st.stop()
    
    ors_api_key = "5b3ce3597851110001cf6248f6655560e2024f9aaef104f6bc121d7b"
    route_path, route_summary = get_route(start, end, ors_api_key)
    driving_time_hr = (route_summary['duration'] / 3600) * 1.5
    
    #client_id = "96dHZVzsAutvtSRMc7fRYSZyuU9bFs6xfRT5CbgKG35S2IpnJhDrowntHp_qoiq54s8BkJstKkHwZuPRgIpQTw=="
    #client_secret = "lrFxI-iSEg-hmrj6DJs0b_PR-f-1HOlBz-YsGkTxUT4RLmavHbW5i4wUxmTD_h3SLLAke2YnZYMJYqfSB8sEFCjCKMvzmWgh"
    client_id = "96dHZVzsAuukZtfZagLKfNcqzXoFF094ZyfjQqjOfprR17jCqYuLNmRto4oA_yan7Jye0lFlO2wHrJyVmu23Gw=="
    client_secret = "lrFxI-iSEg_5Bfm_-_C7psNkJrwfuKA6GeYQzbC4um7j8iR1_M6r4zE0MGKKHaD5IYWoO15DXvYo6aWm3EqAw1gU5eTSXKaT"

    token = get_mapmyindia_token(client_id, client_secret)

    stops = [("Start", route_path[0][0], route_path[0][1])]
    dist_covered = 0
    total_dist_km = 0
    prev_point = route_path[0]
    stop_expanders = [] 

    for point in route_path[1:]:
        seg_dist = geodesic(prev_point, point).km
        dist_covered += seg_dist
        total_dist_km += seg_dist
        prev_point = point

        if dist_covered >= safe_limit_km:
            expander_content = {
                "title": f"🔋 Charging Stop • After {int(total_dist_km)} km",
                "location": f"📍 Suggested Location Near: ({round(point[0], 4)}, {round(point[1], 4)})",
                "chargers_found": [], "pois": {}
            }
            chargers = show_nearby_chargers(point[0], point[1], token)
            if chargers:
                expander_content["chargers_found"].append("✅ **Nearby Charging Stations Found:**")
                for i, c in enumerate(chargers[:5]):
                    name = c.get("placeName", "Charger")
                    addr = c.get("placeAddress", "No address")
                    dist = c.get("distance", "N/A")
                    eloc = c.get("eLoc", "")
                    map_link = f"https://maps.mapmyindia.com/{eloc}" if eloc else "https://maps.mapmyindia.com/"
                    expander_content["chargers_found"].append(
                        f"{i+1}. **{name}** — {addr} ({dist} m) [🔗 Map]({map_link})"
                    )
                ch = chargers[0]
                stops.append((ch.get("placeName", "Charger"), point[0], point[1]))

                poi_categories = {"🍽️ Food": "restaurant", "☕ Cafe": "cafe", "📸 Attractions": "tourist attraction"}
                for label, keyword in poi_categories.items():
                    pois = get_poi(point[0], point[1], token, keyword)
                    if pois:
                        expander_content["pois"][label] = []
                        for p in pois[:3]:
                            name = p.get("placeName", "Unknown place")
                            addr = p.get("placeAddress", "")
                            distance = p.get("distance", "N/A")
                            expander_content["pois"][label].append(f"- **{name}** — {addr} ({distance} m)")
                    else:
                        expander_content["pois"][label] = [f"- No {label.lower()} found nearby."]
            else:
                expander_content["chargers_found"].append("⚠️ No chargers found nearby.")
            
            stop_expanders.append(expander_content)
            dist_covered = 0
            time.sleep(1)

    stops.append(("Destination", route_path[-1][0], route_path[-1][1]))
    num_charging_stops = max(len(stops) - 2, 0)
    charging_time_hr = num_charging_stops * ((0.8 * battery_capacity) / charger_power)
    total_trip_time_hr = driving_time_hr + charging_time_hr
    hours = int(total_trip_time_hr)
    minutes = int((total_trip_time_hr - hours) * 60)

    # --- MAP CREATION ---
    m = folium.Map(location=[start[0], start[1]], zoom_start=7)
    try:
        folium.PolyLine(route_path, weight=5, color="blue", opacity=0.8, tooltip="Planned EV Route").add_to(m)
    except Exception as e:
        st.warning(f"⚠️ Could not draw route line: {e}")

    for idx, (name, lat, lon) in enumerate(stops):
        if idx == 0:
            icon_color, icon_emoji, marker_title = "green", "🚗", "Start Point"
        elif idx == len(stops) - 1:
            icon_color, icon_emoji, marker_title = "red", "🏁", "Destination"
        else:
            icon_color, icon_emoji, marker_title = "orange", "⚡", f"Charging Stop {idx}"
        
        if idx == 0: map_link = f"https://maps.mapmyindia.com/{start[0]},{start[1]}"
        elif idx == len(stops) - 1: map_link = f"https://maps.mapmyindia.com/{end[0]},{end[1]}"
        else:
            eloc = name.split()[-1] if len(name.split()) == 1 else ""
            map_link = f"https://maps.mapmyindia.com/{eloc}" if eloc else f"https://maps.mapmyindia.com/{lat},{lon}"
        
        popup_html = f"""<div style='font-size:14px; line-height:1.6'>
            <b>{icon_emoji} {marker_title}</b><br>
            <b>Name:</b> {name}<br>
            📍 <b>Coordinates:</b> {round(lat, 4)}, {round(lon, 4)}<br>
            <a href="{map_link}" target="_blank">🔗 View in MapmyIndia</a>
        </div>"""
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(m)
    
    # --- 4. STORE ALL RESULTS IN SESSION STATE ---
    st.session_state.trip_results = {
        "metrics": {
            "Total Distance": f"{total_dist_km:.0f} km",
            "Total Time": f"{hours}h {minutes}m",
            "Driving Time": f"{driving_time_hr:.1f} hr",
            "Charging Stops": f"{num_charging_stops} stop(s)"
        },
        "map": m,
        "stop_summary_data": [f"{i+1}. {name} at ({round(lat, 4)}, {round(lon, 4)})" for i, (name, lat, lon) in enumerate(stops)],
        "stop_expanders": stop_expanders
    }
    
    # --- 5. LOGIC IS DONE, SET STATE TO "NOT RUNNING" ---
    st.session_state.trip_in_progress = False
    
    # --- 6. EXPLICITLY CLEAR THE SPINNER AND RERUN ---
    placeholder.empty()
    st.rerun()

# --- RESULTS DISPLAY BLOCK ---
# This block runs ONLY after logic is done and 'trip_results' exists
if st.session_state.trip_results:
    
    st.success("Your trip plan is ready!")
    
    results = st.session_state.trip_results
    
    # --- METRICS (KPIs) ---
    st.subheader("Trip Summary")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Total Distance", results["metrics"]["Total Distance"])
    metric_cols[1].metric("Total Time", results["metrics"]["Total Time"])
    metric_cols[2].metric("Driving Time", results["metrics"]["Driving Time"])
    metric_cols[3].metric("Charging Stops", results["metrics"]["Charging Stops"])

    # --- TABS FOR RESULTS ---
    tab1, tab2 = st.tabs(["🗺️ Route Visualization", "🔋 Stop-by-Stop Details"])

    with tab1:
        st.subheader("Interactive Route Map")
        st_folium(results["map"], width=1000, height=600, returned_objects=[])

    with tab2:
        st.subheader("Planned Stops & POIs")
        
        st.subheader("📍 Stop Summary")
        for line in results["stop_summary_data"]:
            st.write(line)
        
        st.markdown("---")
        st.subheader("⭐ Explore while your EV charges")
        
        if not results["stop_expanders"]:
            st.info("No charging stops were needed for this trip.")
        
        for stop_data in results["stop_expanders"]:
            with st.expander(stop_data["title"]):
                st.markdown(stop_data["location"])
                
                for charger_line in stop_data["chargers_found"]:
                    st.markdown(charger_line, unsafe_allow_html=True)
                
                st.markdown("---")
                
                for label, poi_list in stop_data["pois"].items():
                    st.markdown(f"**{label}:**")
                    for poi_line in poi_list:
                        st.write(poi_line)