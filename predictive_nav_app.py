import streamlit as st
import pandas as pd
import numpy as np
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
# SESSION NAVIGATION FIX ⭐⭐⭐
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# --------------------------------------------------
# PREMIUM STYLE
# --------------------------------------------------
st.markdown("""
<style>
header, footer, #MainMenu {visibility:hidden;}

body {
    background: linear-gradient(180deg,#0b0f17,#05070c);
}

.title{
    text-align:center;
    font-size:55px;
    font-weight:900;
    color:#00eaff;
    text-shadow:0 0 15px #00eaff;
}

section[data-testid="stSidebar"]{
    background:#0f1624;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR (NEVER DISAPPEARS)
# --------------------------------------------------
st.sidebar.title("MELLOWTECH")

pages = [
    "Dashboard",
    "Predict Traffic",
    "Smart Routes",
    "Live Map",
    "Reports",
    "Profile"
]

selected = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = selected

# --------------------------------------------------
# DATA ENGINE
# --------------------------------------------------
np.random.seed(42)
locations=["Home","Work","School","Gym","Mall"]
hours=np.arange(6,22)

traffic_matrix=pd.DataFrame(
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

def get_weather(lat,lon):
    url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    return requests.get(url).json()["current_weather"]

weather_map={
0:"Clear",2:"Partly Cloudy",3:"Overcast",
45:"Fog",61:"Rain",63:"Moderate Rain",
65:"Heavy Rain",95:"Thunderstorm"
}

bad_weather=[45,61,63,65,95]

# ==================================================
# DASHBOARD
# ==================================================
if st.session_state.page=="Dashboard":

    st.markdown("<div class='title'>MELLOWTECH</div>",unsafe_allow_html=True)

    timezone=pytz.timezone("Africa/Johannesburg")
    current_time=dt.now(timezone).strftime("%H:%M:%S")

    c1,c2,c3=st.columns(3)
    c1.metric("System","ONLINE")
    c2.metric("Time",current_time)
    c3.metric("AI Engine","Running")

# ==================================================
# PREDICT TRAFFIC
# ==================================================
elif st.session_state.page=="Predict Traffic":

    st.header("AI Traffic Prediction")

    col1,col2,col3=st.columns(3)

    start=col1.selectbox("Start",locations)
    end=col2.selectbox("Destination",locations)
    leave_time=col3.slider("Departure",6,22,8)

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

    df=pd.DataFrame({
        "Hour":forecast.keys(),
        "Congestion %":forecast.values()
    })

    st.table(df)
    st.line_chart(pd.Series(forecast),use_container_width=True)

    best=min(forecast,key=forecast.get)
    st.success(f"Optimal Departure: {best}:00")

# ==================================================
# SMART ROUTES
# ==================================================
elif st.session_state.page=="Smart Routes":

    st.header("Smart Route Optimization")

    route=st.radio(
        "Route Mode",
        ["Fastest Route","Collective AI Route"]
    )

    if route=="Collective AI Route":
        st.success("You helped reduce city congestion")
        st.balloons()

# ==================================================
# LIVE MAP
# ==================================================
elif st.session_state.page=="Live Map":

    st.header("Live Navigation Map")

    map_data=pd.DataFrame({
        "lat":[coords["Home"][0],coords["Work"][0]],
        "lon":[coords["Home"][1],coords["Work"][1]]
    })

    st.map(map_data,zoom=14)

# ==================================================
# REPORTS
# ==================================================
elif st.session_state.page=="Reports":

    st.header("Report Traffic Issue")

    issue=st.selectbox(
        "Issue",
        ["Accident","Traffic Jam","Roadblock","Pothole"]
    )

    if st.button("Submit"):
        st.success("Report Submitted")

# ==================================================
# PROFILE
# ==================================================
elif st.session_state.page=="Profile":

    st.header("User Profile")

    st.text_input("Home Address")
    st.text_input("Work Address")

    st.success("Profile Active")
