# predictive_nav_app.py

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import pytz
from datetime import datetime as dt

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="MelloTech Predictive Navigation",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------
# DARK UI + APP SKIN
# --------------------------
st.markdown("""
<style>

header, [data-testid="stHeader"], #MainMenu, footer {
    display:none;
}

body {
    background-color:#121212;
}

.block-container {
    max-width:900px;
    margin:auto;
    padding:2rem;
    background:#1e1e1e;
    border-radius:15px;
    box-shadow:0 0 20px rgba(0,0,0,0.7);
    color:white;
    position:relative;
}

/* Floating Logo */
#floating-logo{
    position:absolute;
    top:20px;
    left:20px;
    width:80px;
    animation:float-spin 4s linear infinite;
}

@keyframes float-spin{
    0%{transform:translateY(0) rotate(0);}
    50%{transform:translateY(-10px) rotate(180deg);}
    100%{transform:translateY(0) rotate(360deg);}
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# WORKING GOOGLE DRIVE LOGO
# --------------------------
logo_url = "https://drive.google.com/thumbnail?id=1pkJLpuvzzaGvAd4ESAiPYiAIphe5JV-h&sz=w1000"

st.markdown(
    f'<img src="{logo_url}" id="floating-logo">',
    unsafe_allow_html=True
)

# --------------------------
# TITLE
# --------------------------
st.title("🚗 MelloTech Predictive Navigation")
st.write(
    "AI predictive congestion, optimal departure time, live weather intelligence and smart routing."
)

# --------------------------
# SIMULATED TRAFFIC DATA
# --------------------------
np.random.seed(42)

locations = ["Home","Work","School","Gym","Mall"]
hours = np.arange(6,22)

traffic_matrix = pd.DataFrame(
    np.random.rand(len(locations),len(hours)),
    index=locations,
    columns=hours
)

# --------------------------
# WEATHER API
# --------------------------
def get_weather(lat,lon):
    url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data=requests.get(url).json()
    cw=data["current_weather"]

    return {
        "temperature":cw["temperature"],
        "windspeed":cw["windspeed"],
        "winddir":cw["winddirection"],
        "code":cw["weathercode"]
    }

weather_map={
0:"Clear",
2:"Partly Cloudy",
3:"Overcast",
45:"Fog",
61:"Rain",
63:"Moderate Rain",
65:"Heavy Rain",
71:"Snow",
73:"Moderate Snow",
75:"Heavy Snow",
95:"Thunderstorm"
}

# --------------------------
# USER INPUTS
# --------------------------
c1,c2,c3=st.columns(3)

with c1:
    start=st.selectbox("Start location",locations)

with c2:
    end=st.selectbox("Destination",locations)

with c3:
    commute_day=st.date_input(
        "Commute date",
        datetime.date.today()
    )

preferred_leave_time=st.slider(
    "Preferred leave hour",
    6,22,8
)

# --------------------------
# COORDINATES
# --------------------------
coords={
"Home":(-25.7461,28.1881),
"Work":(-25.7580,28.1890),
"School":(-25.7500,28.2000),
"Gym":(-25.7400,28.1800),
"Mall":(-25.7450,28.1950)
}

start_lat,start_lon=coords[start]
end_lat,end_lon=coords[end]

# --------------------------
# CURRENT TIME
# --------------------------
tz=pytz.timezone("Africa/Johannesburg")
current_time=dt.now(tz).strftime("%H:%M:%S")

st.subheader("⏱ Current Time")
st.write(current_time)

# --------------------------
# WEATHER DISPLAY
# --------------------------
weather=get_weather(start_lat,start_lon)

st.subheader("🌦 Live Weather")

st.write(f"Temperature: {weather['temperature']}°C")
st.write(f"Wind Speed: {weather['windspeed']} km/h")
st.write(f"Condition: {weather_map.get(weather['code'],'Unknown')}")

if weather['code'] in [45,61,63,65,71,73,75,95]:
    st.warning("⚠️ Bad weather detected — traffic may slow.")
else:
    st.success("✅ Weather conditions good.")

# --------------------------
# CONGESTION MODEL
# --------------------------
def predict_congestion(hour):

    base=traffic_matrix.loc[start,hour]

    rush=0.5 if hour in [7,8,17,18] else 0

    bad_weather=0.2 if weather['code'] in [45,61,63,65,71,73,75,95] else 0

    return min(base+rush+bad_weather,1.0)

forecast_hours=np.arange(preferred_leave_time,
                         preferred_leave_time+3)

forecast_data={
h:predict_congestion(h)
for h in forecast_hours
}

# --------------------------
# USER FRIENDLY DISPLAY
# --------------------------
forecast_percent={
h:round(v*100)
for h,v in forecast_data.items()
}

def traffic_label(v):
    if v<30:
        return "🟢 Light Traffic"
    elif v<60:
        return "🟡 Moderate Traffic"
    else:
        return "🔴 Heavy Traffic"

forecast_labels={
h:traffic_label(v)
for h,v in forecast_percent.items()
}

st.subheader("🚦 Predicted Congestion")

congestion_df=pd.DataFrame({
"Hour":forecast_percent.keys(),
"Congestion (%)":forecast_percent.values(),
"Traffic Level":forecast_labels.values()
})

st.table(congestion_df)

st.bar_chart(pd.Series(forecast_percent))

# --------------------------
# OPTIMAL TIME
# --------------------------
best_time=min(forecast_data,
              key=forecast_data.get)

st.success(f"✅ Optimal departure time: {best_time}:00")

# --------------------------
# ROUTE SELECTION
# --------------------------
route_choice=st.radio(
"Recommended Route",
["Fastest individually",
 "Less congested collectively"]
)

if route_choice=="Less congested collectively":
    st.info("You help reduce city traffic congestion!")

# --------------------------
# REWARD SYSTEM
# --------------------------
if route_choice=="Less congested collectively" \
and best_time!=preferred_leave_time:

    st.balloons()
    st.success("🎉 You earned 10 Smart Mobility Points!")

# --------------------------
# MAP
# --------------------------
st.subheader("🗺 Route Map")

map_data=pd.DataFrame({
"lat":[start_lat,end_lat],
"lon":[start_lon,end_lon]
})

st.map(map_data,zoom=14)
