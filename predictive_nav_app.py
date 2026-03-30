import streamlit as st
import pandas as pd
import numpy as np
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
# SESSION STATE
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

# --------------------------
# STYLE (BLUE + RED LIGHT)
# --------------------------
st.markdown("""
<style>

/* Hide Streamlit branding */
header, #MainMenu, footer {visibility:hidden;}

body{
background:#121212;
color:white;
}

/* MAIN CARD */
.block-container{
max-width:950px;
margin:auto;
background:#1e1e1e;
padding:2rem;
border-radius:20px;
box-shadow:
0 0 20px rgba(0,255,255,0.2),
0 0 40px rgba(255,0,60,0.15);
}

/* TITLE */
#title{
font-size:4rem;
font-weight:900;
text-align:center;
color:#00f0ff;
text-shadow:
0 0 10px #00f0ff,
0 0 25px #0099ff,
0 0 45px #ff003c;
}

/* MENU BUTTON */
.menu-btn button{
background:#2a2a2a;
border-radius:10px;
font-size:22px;
}

/* MENU STYLE */
.menu{
background:#181818;
padding:20px;
border-radius:15px;
box-shadow:0 0 25px rgba(0,0,0,0.8);
}

/* SECTION CARD */
.section{
background:#2b2b2b;
padding:25px;
border-radius:15px;
margin-top:25px;
box-shadow:0 0 15px rgba(0,0,0,0.6);
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER
# --------------------------
col1,col2 = st.columns([1,6])

with col1:
    if st.button("☰"):
        st.session_state.menu_open = not st.session_state.menu_open

with col2:
    st.markdown("<div id='title'>MELLOWTECH</div>",unsafe_allow_html=True)

# --------------------------
# GMAIL STYLE MENU
# --------------------------
if st.session_state.menu_open:

    st.markdown("<div class='menu'>",unsafe_allow_html=True)

    if st.button("🏠 Dashboard"):
        st.session_state.page="Dashboard"

    if st.button("🚦 Predict Traffic"):
        st.session_state.page="Predict"

    if st.button("🗺 Navigation Map"):
        st.session_state.page="Map"

    if st.button("📊 Analytics"):
        st.session_state.page="Analytics"

    if st.button("👤 Profile"):
        st.session_state.page="Profile"

    st.markdown("</div>",unsafe_allow_html=True)

# --------------------------
# DATA
# --------------------------
np.random.seed(42)

locations=["Home","Work","School","Gym","Mall"]

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

def traffic_light(v):
    if v<30:
        return "🟢 Light Traffic"
    elif v<60:
        return "🟡 Moderate Traffic"
    else:
        return "🔴 Heavy Traffic"

# =====================================================
# PAGE ROUTING
# =====================================================

# ---------------- DASHBOARD ----------------
if st.session_state.page=="Dashboard":

    st.markdown("<div class='section'>",unsafe_allow_html=True)

    timezone=pytz.timezone("Africa/Johannesburg")
    current_time=dt.now(timezone).strftime("%H:%M:%S")

    st.header("Dashboard")
    st.metric("Current Time",current_time)
    st.success("Traffic Intelligence Online")

    st.markdown("</div>",unsafe_allow_html=True)

# ---------------- PREDICT ----------------
elif st.session_state.page=="Predict":

    st.markdown("<div class='section'>",unsafe_allow_html=True)

    st.header("Predict Traffic")

    col1,col2=st.columns(2)

    with col1:
        start=st.selectbox("Start Location",locations)

    with col2:
        end=st.selectbox("Destination",locations)

    leave_time=st.slider("Leave Time",6,22,8)

    lat,lon=coords[start]
    weather=get_weather(lat,lon)

    st.write(f"🌦 Temperature: {weather['temperature']}°C")

    congestion=np.random.randint(10,90,3)

    df=pd.DataFrame({
        "Hour":[leave_time+i for i in range(3)],
        "Congestion %":congestion
    })

    df["Traffic"]=df["Congestion %"].apply(traffic_light)

    st.table(df)
    st.line_chart(df.set_index("Hour"))

    best=df.loc[df["Congestion %"].idxmin(),"Hour"]

    st.markdown(
        f"<h2 style='color:#00f0ff'>Optimal Departure: {best}:00</h2>",
        unsafe_allow_html=True
    )

    st.markdown("</div>",unsafe_allow_html=True)

# ---------------- MAP ----------------
elif st.session_state.page=="Map":

    st.markdown("<div class='section'>",unsafe_allow_html=True)

    st.header("Live Navigation")

    start="Home"
    end="Work"

    map_data=pd.DataFrame({
        "lat":[coords[start][0],coords[end][0]],
        "lon":[coords[start][1],coords[end][1]]
    })

    st.map(map_data,zoom=14)

    st.markdown("</div>",unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
elif st.session_state.page=="Analytics":

    st.markdown("<div class='section'>",unsafe_allow_html=True)

    st.header("Traffic Analytics")

    data=np.random.randint(20,100,24)

    analytics=pd.DataFrame({
        "Hour":range(24),
        "Traffic":data
    })

    st.line_chart(analytics.set_index("Hour"))

    st.info("AI predicts congestion behaviour.")

    st.markdown("</div>",unsafe_allow_html=True)

# ---------------- PROFILE ----------------
elif st.session_state.page=="Profile":

    st.markdown("<div class='section'>",unsafe_allow_html=True)

    st.header("Profile")

    st.write("User: MELLOWTECH Driver")
    st.success("Reward Points: 120")

    if st.button("Sync Mobility Data"):
        st.balloons()

    st.markdown("</div>",unsafe_allow_html=True)
