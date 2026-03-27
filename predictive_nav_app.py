# predictive_nav_app_decorated.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests

# Optional map imports
try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    st.warning("⚠️ Map display skipped because 'folium' or 'streamlit_folium' is not installed. Run: pip install folium streamlit-folium")

# Optional auto-refresh
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60000, key="refresh")
except ImportError:
    st.info("Autorefresh not available. Install 'streamlit-autorefresh' to enable it.")

# --------------------------
# Custom CSS for styling
# --------------------------
st.markdown("""
<style>
/* Page background */
body, .block-container {background-color: #f9f9f9; font-family: 'Arial', sans-serif;}

/* Title */
h1, h2, h3, h4 {color: #1a73e8; font-weight: bold;}

/* Cards */
.card {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

/* Bar chart colors */
[data-testid="stBarChart"] svg rect { fill: #1a73e8 !important; }

</style>
""", unsafe_allow_html=True)

# --------------------------
# App Title
# --------------------------
st.markdown("<h1>🚗 Smart Predictive Navigation</h1>", unsafe_allow_html=True)
st.markdown("Predictive congestion, optimized departure, collective route shaping, rewards, live weather, and map! 🌦️🗺️")

# --------------------------
# Simulated traffic
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
    response = requests.get(url)
    data = response.json()
    weather_code = data["current_weather"]["weathercode"]
    temperature = data["current_weather"]["temperature"]
    wind_speed = data["current_weather"]["windspeed"]
    wind_dir = data["current_weather"]["winddirection"]
    return {"weather_code": weather_code, "temperature": temperature, "wind_speed": wind_speed, "wind_dir": wind_dir}

weather_map = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    95: "Thunderstorm", 99: "Thunderstorm with hail"
}

# --------------------------
# User inputs
# --------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🛣️ Your commute settings")
start = st.selectbox("Start location:", locations)
end = st.selectbox("Destination:", locations)
commute_day = st.date_input("Commute date:", datetime.date.today())
preferred_leave_time = st.slider("Preferred leave time:", 6, 22, 8)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Dummy coordinates
# --------------------------
coords = {
    "Home": (-25.7461, 28.1881),
    "Work": (-25.7580, 28.1890),
    "School": (-25.7500, 28.2000),
    "Gym": (-25.7400, 28.1800),
    "Mall": (-25.7450, 28.1950)
}
start_lat, start_lon = coords[start]
end_lat, end_lon = coords[end]

# --------------------------
# Weather display
# --------------------------
weather_data = get_weather(start_lat, start_lon)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🌦️ Current Weather at Start Location")
st.markdown(f"**Temperature:** {weather_data['temperature']} °C  🌡️")
st.markdown(f"**Wind:** {weather_data['wind_speed']} km/h, Direction: {weather_data['wind_dir']}° 💨")
st.markdown(f"**Condition:** {weather_map.get(weather_data['weather_code'], 'Unknown')} ☁️")

if weather_data["weather_code"] in [45,48,61,63,65,71,73,75,95,99]:
    st.warning("⚠️ Bad weather detected — traffic may be slower!")
else:
    st.success("✅ Weather conditions are good for travel.")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Predictive congestion
# --------------------------
def predict_congestion(start, end, hour):
    base = traffic_matrix.loc[start, hour]
    rush_hour = 1 if hour in [7, 8, 17, 18] else 0
    predicted = min(base + rush_hour*0.5, 1.0)
    if weather_data["weather_code"] in [45,48,61,63,65,71,73,75,95,99]:
        predicted = min(predicted+0.2, 1.0)
    return predicted

forecast_hours = np.arange(preferred_leave_time, preferred_leave_time+3)
forecast_data = {h: predict_congestion(start, end, h) for h in forecast_hours}

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Predicted congestion (0=low, 1=high)")
st.bar_chart(pd.Series(forecast_data))
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Optimal departure
# --------------------------
best_time = min(forecast_data, key=forecast_data.get)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.success(f"⏰ Optimal departure time: {best_time}:00")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Collective route shaping
# --------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
routes = ["Route A (fastest individually)", "Route B (less congested collectively)"]
st.subheader("🗺️ Recommended route")
route_choice = st.radio("Choose your route:", routes)
if route_choice == routes[1]:
    st.info("👍 You are helping reduce overall congestion!")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Rewards
# --------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🎁 Your traffic rewards")
if route_choice == routes[1] and best_time != preferred_leave_time:
    st.balloons()
    st.success("🎉 You earned 10 reward points!")
else:
    st.info("Take the collective-optimized route + optimal departure time next time for rewards.")
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Map display
# --------------------------
if FOLIUM_AVAILABLE:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🗺️ Route Map")
    map_center = [(start_lat+end_lat)/2, (start_lon+end_lon)/2]
    m = folium.Map(location=map_center, zoom_start=14)
    folium.Marker([start_lat, start_lon], tooltip=start, popup=f"Start: {start}", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker([end_lat, end_lon], tooltip=end, popup=f"Destination: {end}", icon=folium.Icon(color="red", icon="flag")).add_to(m)
    folium.PolyLine([[start_lat,start_lon],[end_lat,end_lon]], color="blue", weight=4, opacity=0.7).add_to(m)
    st_folium(m, width=700, height=500)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.write("---")
st.markdown("⚠️ This app now includes **beautifully styled cards, emojis, live weather, predictive congestion, route map, and rewards!**")
