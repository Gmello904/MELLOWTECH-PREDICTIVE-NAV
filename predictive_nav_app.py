import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import pytz
from datetime import datetime as dt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# PREMIUM UI DESIGN
# --------------------------------------------------
st.markdown("""
<style>

/* Remove Streamlit branding */
header, footer, #MainMenu {visibility:hidden;}

/* Background */
body {
    background: linear-gradient(180deg,#0b0f17,#05070c);
}

/* Main card */
.block-container{
    max-width:1100px;
    margin:auto;
    padding:2.5rem;
    background:#121826;
    border-radius:20px;
    box-shadow:0 0 40px rgba(0,0,0,0.8);
}

/* MELLOWTECH TITLE */
.title{
    text-align:center;
    font-size:70px;
    font-weight:900;
    color:#00eaff;
    text-shadow:
        0 0 10px #00eaff,
        0 0 25px #00bfff,
        0 0 50px #0077ff;
}

/* Subtitle */
.subtitle{
    text-align:center;
    color:#9aa4b2;
    margin-bottom:30px;
    font-size:18px;
}

/* Cards */
.metric-card{
    background:#1b2335;
    padding:20px;
    border-radius:15px;
    text-align:center;
}

/* Mobile responsiveness */
@media(max-width:768px){
.title{font-size:42px;}
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Predictive Navigation & Smart Mobility Intelligence</div>", unsafe_allow_html=True)

# --------------------------------------------------
# SIMULATED DATA ENGINE
# --------------------------------------------------
np.random.seed(42)

locations = ["Home","Work","School","Gym","Mall"]
hours = np.arange(6,22)

traffic_matrix = pd.DataFrame(
    np.random.rand(len(locations),len(hours)),
    index=locations,
    columns=hours
)

# --------------------------------------------------
# WEATHER API
# --------------------------------------------------
def get_weather(lat,lon):
    url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data=requests.get(url).json()
    return data["current_weather"]

weather_map={
0:"Clear",
2:"Partly Cloudy",
3:"Overcast",
45:"Fog",
61:"Rain",
63:"Moderate Rain",
65:"Heavy Rain",
95:"Thunderstorm"
}

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
col1,col2,col3=st.columns(3)

with col1:
    start=st.selectbox("Start Location",locations)

with col2:
    end=st.selectbox("Destination",locations)

with col3:
    commute_date=st.date_input("Travel Date",datetime.date.today())

leave_time=st.slider("Preferred Departure Time",6,22,8)

# --------------------------------------------------
# COORDINATES
# --------------------------------------------------
coords={
"Home":(-25.7461,28.1881),
"Work":(-25.7580,28.1890),
"School":(-25.7500,28.2000),
"Gym":(-25.7400,28.1800),
"Mall":(-25.7450,28.1950)
}

lat,lon=coords[start]

# --------------------------------------------------
# LIVE STATUS DASHBOARD
# --------------------------------------------------
timezone=pytz.timezone("Africa/Johannesburg")
current_time=dt.now(timezone).strftime("%H:%M:%S")

colA,colB=st.columns(2)

with colA:
    st.subheader("Current Time")
    st.success(current_time)

with colB:
    weather=get_weather(lat,lon)
    st.subheader("Live Weather")
    st.info(weather_map.get(weather["weathercode"],"Unknown"))

# --------------------------------------------------
# TRAFFIC AI PREDICTION
# --------------------------------------------------
bad_weather=[45,61,63,65,95]

def predict(hour):
    base=traffic_matrix.loc[start,hour]
    rush=0.5 if hour in [7,8,17,18] else 0
    weather_penalty=0.2 if weather["weathercode"] in bad_weather else 0
    return min(base+rush+weather_penalty,1)

forecast_hours=np.arange(leave_time,leave_time+3)
forecast={h:round(predict(h)*100) for h in forecast_hours}

# Traffic Lights
def traffic_label(v):
    if v<30:
        return "🟢 Light Traffic"
    elif v<60:
        return "🟡 Moderate Traffic"
    else:
        return "🔴 Heavy Traffic"

labels={h:traffic_label(v) for h,v in forecast.items()}

df=pd.DataFrame({
"Hour":forecast.keys(),
"Congestion %":forecast.values(),
"Traffic":labels.values()
})

st.subheader("AI Traffic Forecast")
st.table(df)

st.line_chart(pd.Series(forecast),use_container_width=True)

# --------------------------------------------------
# OPTIMAL DEPARTURE
# --------------------------------------------------
best=min(forecast,key=forecast.get)

st.markdown(
f"<h2 style='text-align:center;color:#00eaff'>Optimal Departure Time: {best}:00</h2>",
unsafe_allow_html=True
)

# --------------------------------------------------
# SMART ROUTE SYSTEM
# --------------------------------------------------
route=st.radio(
"Route Optimization Mode",
["Fastest Route","Collective Smart Route"]
)

if route=="Collective Smart Route":
    st.info("You contribute to reducing Gauteng congestion.")

# --------------------------------------------------
# REWARD SYSTEM
# --------------------------------------------------
if route=="Collective Smart Route" and best!=leave_time:
    st.balloons()
    st.success("🎉 Smart Mobility Reward +10 Points")

# --------------------------------------------------
# MAP VISUALIZATION
# --------------------------------------------------
st.subheader("Live Route Map")

map_data=pd.DataFrame({
"lat":[coords[start][0],coords[end][0]],
"lon":[coords[start][1],coords[end][1]]
})

st.map(map_data,zoom=14)
