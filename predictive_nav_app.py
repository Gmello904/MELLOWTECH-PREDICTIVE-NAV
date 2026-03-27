# predictive_nav_app.py
# Streamlit app simulating predictive navigation with rewards + real-time weather

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests

# --------------------------
# 🔥 HIDE TOOLBAR
# --------------------------
st.markdown("""
<style>
header, [data-testid="stHeader"], [data-testid="stToolbar"],
#MainMenu, footer {
    display: none !important;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# App Title
# --------------------------
st.title("🚗 Smart Predictive Navigation Prototype")
st.write("Simulating predictive congestion, optimized departure time, collective route shaping, rewards, and live weather awareness!")

# --------------------------
# Simulated traffic data
# --------------------------
np.random.seed(42)
locations = ["Home", "Work", "School", "Gym", "Mall"]
hours = np.arange(6, 22)  # 6 AM to 10 PM

traffic_matrix = pd.DataFrame(
    np.random.rand(len(locations), len(hours)),
    index=locations,
    columns=hours
)

# --------------------------
# Weather Function (Open-Meteo)
# --------------------------
def get_weather(lat, lon):
    """Fetches current weather from Open-Meteo for given coordinates."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    weather_code = data["current_weather"]["weathercode"]
    temperature = data["current_weather"]["temperature"]
    wind_speed = data["current_weather"]["windspeed"]
    wind_dir = data["current_weather"]["winddirection"]

    return {
        "weather_code": weather_code,
        "temperature": temperature,
        "wind_speed": wind_speed,
        "wind_dir": wind_dir
    }

# Map numeric weather codes to descriptions
weather_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    95: "Thunderstorm",
    99: "Thunderstorm with hail"
}

# --------------------------
# User Inputs
# --------------------------
st.subheader("Your commute settings")
start = st.selectbox("Start location:", locations)
end = st.selectbox("Destination:", locations)
commute_day = st.date_input("Commute date:", datetime.date.today())
preferred_leave_time = st.slider("Preferred leave time:", 6, 22, 8)

# --------------------------
# Map locations to coordinates (dummy for now)
# You can replace with Geocoding API later
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
# Live Weather
# --------------------------
st.subheader("🌦 Current Weather at Start Location")
weather_data = get_weather(start_lat, start_lon)

st.write(f"Temperature: {weather_data['temperature']} °C")
st.write(f"Wind: {weather_data['wind_speed']} km/h, Direction: {weather_data['wind_dir']}°")
st.write(f"Condition: {weather_map.get(weather_data['weather_code'], 'Unknown')}")

# Optional traffic impact warning
if weather_data["weather_code"] in [45,48,61,63,65,71,73,75,95,99]:
    st.warning("⚠️ Bad weather detected — traffic may be slower!")
else:
    st.success("✅ Weather conditions are good for travel.")

# --------------------------
# Predictive congestion (dummy)
# --------------------------
def predict_congestion(start, end, hour):
    base = traffic_matrix.loc[start, hour]
    rush_hour = 1 if hour in [7, 8, 17, 18] else 0
    predicted = min(base + rush_hour * 0.5, 1.0)

    # Optional: increase congestion slightly if weather is bad
    if weather_data["weather_code"] in [45,48,61,63,65,71,73,75,95,99]:
        predicted = min(predicted + 0.2, 1.0)
    return predicted

st.subheader("Predicted congestion levels for your route (0=low, 1=high)")
forecast_hours = np.arange(preferred_leave_time, preferred_leave_time+3)
forecast_data = {h: predict_congestion(start, end, h) for h in forecast_hours}
st.bar_chart(pd.Series(forecast_data))

# --------------------------
# Personalized departure time optimization
# --------------------------
best_time = min(forecast_data, key=forecast_data.get)
st.success(f"✅ Optimal departure time to reduce your commute: {best_time}:00")

# --------------------------
# Collective route shaping
# --------------------------
routes = ["Route A (fastest individually)", "Route B (less congested collectively)"]
st.subheader("Recommended route based on collective optimization")
route_choice = st.radio("Choose your route:", routes)

if route_choice == routes[1]:
    st.info("👍 You are helping reduce overall congestion!")

# --------------------------
# Rewards for coordinated behavior
# --------------------------
st.subheader("Your traffic rewards")
if route_choice == routes[1] and best_time != preferred_leave_time:
    st.balloons()
    st.success("🎉 You earned 10 reward points for coordinated commuting!")
else:
    st.info("Take the collective-optimized route to earn rewards next time.")

# --------------------------
# Footer
# --------------------------
st.write("---")
st.write("⚠️ This prototype now includes **real-time weather data** to make predictive congestion more realistic.")
