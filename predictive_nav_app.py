import streamlit as st
import pandas as pd
import numpy as np
import requests
import pytz
from datetime import datetime as dt

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# STYLE (BLUE GLOW + CLEAN UI)
# ------------------------------------------------
st.markdown("""
<style>

/* remove streamlit branding */
header, footer, #MainMenu {visibility:hidden;}

body{
background:#0b0f17;
color:white;
}

/* title glow */
.title{
text-align:center;
font-size:60px;
font-weight:900;
color:#00eaff;
text-shadow:0 0 20px #00eaff;
margin-bottom:20px;
}

/* sidebar */
section[data-testid="stSidebar"]{
background:#111827;
}

/* cards */
.block-container{
padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# APP TITLE
# ------------------------------------------------
st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR NAVIGATION ⭐ (MAIN FIX)
# ------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Predict Traffic",
        "Smart Routes",
        "Live Map",
        "Reports",
        "Profile"
    ]
)

# ------------------------------------------------
# DATA
# ------------------------------------------------
locations=["Home","Work","School","Gym","Mall"]

coords={
"Home":(-25.7461,28.1881),
"Work":(-25.7580,28.1890),
"School":(-25.7500,28.2000),
"Gym":(-25.7400,28.1800),
"Mall":(-25.7450,28.1950)
}

np.random.seed(42)
hours=np.arange(6,22)
traffic=pd.DataFrame(
np.random.rand(len(locations),len(hours)),
index=locations,
columns=hours
)

def weather(lat,lon):
    url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    return requests.get(url).json()["current_weather"]

# =====================================================
# DASHBOARD
# =====================================================
if page=="Dashboard":

    st.header("AI Mobility Dashboard")

    tz=pytz.timezone("Africa/Johannesburg")
    time=dt.now(tz).strftime("%H:%M:%S")

    c1,c2,c3=st.columns(3)

    c1.metric("System","ONLINE")
    c2.metric("Time",time)
    c3.metric("AI Engine","Running")

# =====================================================
# PREDICT TRAFFIC
# =====================================================
elif page=="Predict Traffic":

    st.header("Predict Traffic Congestion")

    col1,col2,col3=st.columns(3)

    start=col1.selectbox("Start",locations)
    end=col2.selectbox("Destination",locations)
    leave=col3.slider("Departure Time",6,22,8)

    lat,lon=coords[start]
    w=weather(lat,lon)

    st.info(f"Temperature: {w['temperature']}°C")

    def predict(hour):
        rush=0.5 if hour in [7,8,17,18] else 0
        return min(traffic.loc[start,hour]+rush,1)

    forecast={h:round(predict(h)*100) for h in range(leave,leave+3)}

    df=pd.DataFrame({
        "Hour":forecast.keys(),
        "Congestion %":forecast.values()
    })

    st.table(df)
    st.line_chart(pd.Series(forecast))

    best=min(forecast,key=forecast.get)
    st.success(f"Optimal departure: {best}:00")

# =====================================================
# SMART ROUTES
# =====================================================
elif page=="Smart Routes":

    st.header("Smart Route AI")

    mode=st.radio(
        "Route Mode",
        ["Fastest Route","Collective AI Route"]
    )

    if mode=="Collective AI Route":
        st.success("You helped reduce congestion")
        st.balloons()

# =====================================================
# LIVE MAP
# =====================================================
elif page=="Live Map":

    st.header("Live Navigation")

    map_data=pd.DataFrame({
        "lat":[coords["Home"][0],coords["Work"][0]],
        "lon":[coords["Home"][1],coords["Work"][1]]
    })

    st.map(map_data,zoom=14)

# =====================================================
# REPORTS
# =====================================================
elif page=="Reports":

    st.header("Report Road Issue")

    issue=st.selectbox(
        "Issue Type",
        ["Accident","Traffic Jam","Roadblock","Pothole"]
    )

    if st.button("Submit"):
        st.success("Report Sent")

# =====================================================
# PROFILE
# =====================================================
elif page=="Profile":

    st.header("User Profile")

    st.text_input("Home Location")
    st.text_input("Work Location")

    st.success("Profile Active")
