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
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PREMIUM DESIGN
# --------------------------------------------------
st.markdown("""
<style>

/* Hide Streamlit branding */
header, footer, #MainMenu {visibility:hidden;}

/* Background */
body {
    background: linear-gradient(180deg,#0b0f17,#05070c);
}

/* Main container */
.block-container{
    padding:2rem;
    max-width:1200px;
}

/* Sidebar styling */
section[data-testid="stSidebar"]{
    background:#0f1624;
}

/* Title */
.title{
    text-align:center;
    font-size:60px;
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
    margin-bottom:20px;
}

/* Mobile */
@media(max-width:768px){
.title{font-size:40px;}
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("MELLOWTECH")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard",
     "Predict Traffic",
     "Smart Routes",
     "Live Map",
     "Reports",
     "Profile"]
)

# --------------------------------------------------
# DATA ENGINE
# --------------------------------------------------
np.random.seed(42)
locations = ["Home","Work","School","Gym","Mall"]
hours = np.arange(6,22)

traffic_matrix = pd.DataFrame(
    np.random.rand(len(locations),len(hours)),
    index=locations,
    columns=hours
)

coords={
"Home":(-25.7461,28.1881),
"Work":(-25.7580,28.1890),
"School":(-25.7500,28.2000),
"Gym":(-25.7400,28.1800),
"Mall":(-25.7450,28.1950)
}

# --------------------------------------------------
# WEATHER
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

bad_weather=[45,61,63,65,95]

# ==================================================
# DASHBOARD
# ==================================================
if menu=="Dashboard":

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AI Mobility Intelligence Dashboard</div>", unsafe_allow_html=True)

    timezone=pytz.timezone("Africa/Johannesburg")
    current_time=dt.now(timezone).strftime("%H:%M:%S")

    col1,col2,col3=st.columns(3)

    col1.metric("System Status","ONLINE")
    col2.metric("Current Time",current_time)
    col3.metric("Active AI Engine","Running")

# ==================================================
# PREDICT TRAFFIC
# ==================================================
elif menu=="Predict Traffic":

    st.header("AI Traffic Prediction")

    col1,col2,col3=st.columns(3)

    with col1:
        start=st.selectbox("Start Location",locations)

    with col2:
        end=st.selectbox("Destination",locations)

    with col3:
        leave_time=st.slider("Departure Time",6,22,8)

    lat,lon=coords[start]
    weather=get_weather(lat,lon)

    st.info(f"Weather: {weather_map.get(weather['weathercode'],'Unknown')}")

    def predict(hour):
        base=traffic_matrix.loc[start,hour]
        rush=0.5 if hour in [7,8,17,18] else 0
        penalty=0.2 if weather["weathercode"] in bad_weather else 0
        return min(base+rush+penalty,1)

    forecast_hours=np.arange(leave_time,leave_time+3)
    forecast={h:round(predict(h)*100) for h in forecast_hours}

    def label(v):
        if v<30:
            return "🟢 Light"
        elif v<60:
            return "🟡 Moderate"
        else:
            return "🔴 Heavy"

    df=pd.DataFrame({
        "Hour":forecast.keys(),
        "Congestion %":forecast.values(),
        "Traffic":[label(v) for v in forecast.values()]
    })

    st.table(df)
    st.line_chart(pd.Series(forecast),use_container_width=True)

    best=min(forecast,key=forecast.get)
    st.success(f"Optimal Departure: {best}:00")

# ==================================================
# SMART ROUTES
# ==================================================
elif menu=="Smart Routes":

    st.header("Smart Route Optimization")

    route=st.radio(
        "Select Mode",
        ["Fastest Individual Route",
         "Collective Smart Route"]
    )

    if route=="Collective Smart Route":
        st.info("You are reducing congestion across Gauteng.")
        st.balloons()
        st.success("Reward +10 Smart Mobility Points")

# ==================================================
# LIVE MAP
# ==================================================
elif menu=="Live Map":

    st.header("Live Route Map")

    start,end="Home","Work"

    map_data=pd.DataFrame({
        "lat":[coords[start][0],coords[end][0]],
        "lon":[coords[start][1],coords[end][1]]
    })

    st.map(map_data,zoom=14)

# ==================================================
# REPORTS
# ==================================================
elif menu=="Reports":

    st.header("Report Traffic Issue")

    issue=st.selectbox(
        "Issue Type",
        ["Accident","Traffic Jam","Roadblock","Pothole"]
    )

    if st.button("Submit Report"):
        st.success("Report Successfully Submitted")

# ==================================================
# PROFILE
# ==================================================
elif menu=="Profile":

    st.header("User Profile")

    st.text_input("Home Location")
    st.text_input("Work Location")

    st.success("Profile Active")
