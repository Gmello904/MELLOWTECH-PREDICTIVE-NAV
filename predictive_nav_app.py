# predictive_nav_app_dark.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import pytz
from datetime import datetime as dt

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="MelloTech Predictive Navigation",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------
# Dark theme CSS
# --------------------------
st.markdown("""
<style>
/* Hide Streamlit branding */
header, [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
    display: none !important;
}

/* General dark background */
body, .block-container {
    background-color: #121212;
    color: #e0e0e0;
    font-family: 'Helvetica', sans-serif;
    padding: 2rem;
}

/* Titles */
h1, h2, h3, .css-1d391kg {
    color: #ffffff;
    font-weight: 600;
}

/* Charts */
.css-10trblm {  /* Streamlit bar chart background */
    background-color: #1e1e1e;
}

/* Selectbox, slider text */
.css-1d391kg, .st-bx {
    color: #e0e0e0;
}

/* Success and info boxes */
.stAlert {
    border-radius: 0.5rem;
    font-size: 1rem;
}

/* Streamlit map container */
.stMap { border-radius: 0.5rem; }

</style>
""", unsafe_allow_html=True)

# --------------------------
# App title
# --------------------------
st.title("MelloTech Predictive Navigation")
st.write("Predictive congestion, optimal departure, collective routes, live weather, time, and map visualization.")

# --------------------------
# Simulated traffic data
# --------------------------
np.random.seed(42)
locations = ["Home", "Work", "School", "Gym", "Mall"]
hours = np.arange(6, 22)
traffic_matrix = pd.DataFrame(np.random.rand(len(locations), len(hours)), index=locations, columns=hours)

# --------------------------
# Weather function
# --------------------------
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()
    cw = data["current_weather"]
    return {
        "temperature": cw["temperature"],
        "windspeed": cw["windspeed"],
        "winddir": cw["winddirection"],
        "code": cw["weathercode"]
    }

weather_map = {
    0:"Clear", 2:"Partly Cloudy", 3:"Overcast", 45:"Fog",
    61:"Rain", 63:"Moderate Rain", 65:"Heavy Rain",
    71:"Snow", 73:"Moderate Snow", 75:"Heavy Snow",
    95:"Thunderstorm"
}

# --------------------------
# User inputs
# --------------------------
col1, col2, col3 = st.columns([1,1,1])
with col1: start = st.selectbox("Start location", locations)
with col2: end = st.selectbox("Destination", locations)
with col3: commute_day = st.date_input("Commute date", datetime.date.today())
preferred_leave_time = st.slider("Preferred leave time", 6, 22, 8)

# --------------------------
# Coordinates (dummy)
# --------------------------
coords = {
    "Home":(-25.7461,28.1881),
    "Work":(-25.7580,28.1890),
    "School":(-25.7500,28.2000),
    "Gym":(-25.7400,28.1800),
    "Mall":(-25.7450,28.1950)
}
start_lat, start_lon = coords[start]
end_lat, end_lon = coords[end]

# --------------------------
# Current Time display
# --------------------------
timezone = pytz.timezone("Africa/Johannesburg")
current_time = dt.now(timezone).strftime("%H:%M:%S")
st.subheader("⏱ Current Time at Start Location")
st.write(current_time)

# --------------------------
# Weather display
# --------------------------
weather = get_weather(start_lat, start_lon)
st.subheader("🌦 Live Weather at Start Location")
st.write(f"Temperature: {weather['temperature']}°C")
st.write(f"Wind: {weather['windspeed']} km/h, Direction: {weather['winddir']}°")
st.write(f"Condition: {weather_map.get(weather['code'], 'Unknown')}")
if weather['code'] in [45,61,63,65,71,73,75,95]:
    st.warning("⚠️ Bad weather detected — traffic may be slower!")
else:
    st.success("✅ Weather conditions are good for travel.")

# --------------------------
# Predictive congestion
# --------------------------
def predict_congestion(hour):
    base = traffic_matrix.loc[start, hour]
    rush = 0.5 if hour in [7,8,17,18] else 0
    bad_weather = 0.2 if weather['code'] in [45,61,63,65,71,73,75,95] else 0
    return min(base + rush + bad_weather, 1.0)

forecast_hours = np.arange(preferred_leave_time, preferred_leave_time+3)
forecast_data = {h: predict_congestion(h) for h in forecast_hours}
st.subheader("Predicted Congestion")
st.bar_chart(pd.Series(forecast_data), use_container_width=True)

# --------------------------
# Optimal departure
# --------------------------
best_time = min(forecast_data, key=forecast_data.get)
st.success(f"Optimal departure time: {best_time}:00")

# --------------------------
# Collective routes
# --------------------------
routes = ["Fastest individually", "Less congested collectively"]
route_choice = st.radio("Recommended route", routes)
if route_choice=="Less congested collectively":
    st.info("You are helping reduce overall congestion!")

# --------------------------
# Rewards
# --------------------------
if route_choice=="Less congested collectively" and best_time != preferred_leave_time:
    st.balloons()
    st.success("🎉 You earned 10 points for coordinated commuting!")

# --------------------------
# Map display
# --------------------------
st.subheader("🗺 Route Map")
map_data = pd.DataFrame({
    'lat': [start_lat, end_lat],
    'lon': [start_lon, end_lon],
    'name': [f"Start: {start}", f"End: {end}"]
})
st.map(map_data, zoom=14)
