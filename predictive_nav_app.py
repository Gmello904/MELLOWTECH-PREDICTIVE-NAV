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
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------
# SHINY DARK THEME
# --------------------------
st.markdown("""
<style>

/* REMOVE STREAMLIT UI */
header, #MainMenu, footer {
    visibility: hidden;
}

/* Background */
body {
    background:#121212;
    color:white;
}

/* App container */
.block-container{
    max-width:1000px;
    margin:auto;
    background:#1e1e1e;
    padding:2rem;
    border-radius:15px;
    box-shadow:0 0 25px rgba(0,0,0,0.8);
}

/* MELLOWTECH glowing title */
#main-title{
    font-size:4rem;
    font-weight:900;
    text-align:center;
    color:#00f0ff;
    text-shadow:
        0 0 5px #00f0ff,
        0 0 10px #0099ff,
        0 0 20px #0066ff;
}

/* Traffic colors */
.light{color:#00ff9f;font-weight:bold;}
.medium{color:#ffd000;font-weight:bold;}
.heavy{color:#ff3b3b;font-weight:bold;}

</style>
""", unsafe_allow_html=True)

# --------------------------
# TITLE
# --------------------------
st.markdown('<div id="main-title">MELLOWTECH</div>', unsafe_allow_html=True)
st.write("Predictive congestion • Smart departure • Live weather • Navigation intelligence")

# --------------------------
# DATA SIMULATION
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
    return cw

# --------------------------
# USER INPUTS
# --------------------------
col1,col2,col3=st.columns(3)

with col1:
    start=st.selectbox("Start",locations)

with col2:
    end=st.selectbox("Destination",locations)

with col3:
    leave_time=st.slider("Leave Time",6,22,8)

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
timezone=pytz.timezone("Africa/Johannesburg")
current_time=dt.now(timezone).strftime("%H:%M:%S")

st.subheader("Current Time")
st.success(current_time)

# --------------------------
# WEATHER DISPLAY
# --------------------------
weather=get_weather(start_lat,start_lon)

st.subheader("Live Weather")
st.write(f"Temperature: {weather['temperature']}°C")
st.write(f"Wind Speed: {weather['windspeed']} km/h")

# --------------------------
# TRAFFIC PREDICTION
# --------------------------
def predict(hour):
    base=traffic_matrix.loc[start,hour]
    rush=0.5 if hour in [7,8,17,18] else 0
    return min(base+rush,1)

forecast_hours=np.arange(leave_time,leave_time+3)

forecast={h:predict(h) for h in forecast_hours}
forecast_percent={h:int(v*100) for h,v in forecast.items()}

def traffic_label(v):
    if v<30:
        return "🟢 Light traffic"
    elif v<60:
        return "🟡 Moderate traffic"
    else:
        return "🔴 Heavy traffic"

labels={h:traffic_label(v) for h,v in forecast_percent.items()}

# --------------------------
# TABLE + CHART
# --------------------------
st.subheader("Predicted Congestion")

df=pd.DataFrame({
"Hour":list(forecast_percent.keys()),
"Congestion %":list(forecast_percent.values()),
"Traffic":list(labels.values())
})

st.table(df)
st.line_chart(df.set_index("Hour"))

# --------------------------
# BEST TIME
# --------------------------
best_time=min(forecast,key=forecast.get)

st.markdown(
f"<h2 style='color:#00f0ff;text-align:center;'>Optimal Departure Time: {best_time}:00</h2>",
unsafe_allow_html=True
)

# --------------------------
# ROUTE SELECTION
# --------------------------
route=st.radio(
"Recommended Route",
["Fastest Individually","Less Congested Collectively"]
)

if route=="Less Congested Collectively":
    st.info("You are helping reduce city congestion!")
    st.balloons()

# --------------------------
# MAP
# --------------------------
st.subheader("Route Map")

map_df=pd.DataFrame({
"lat":[start_lat,end_lat],
"lon":[start_lon,end_lon]
})

st.map(map_df,zoom=14)
