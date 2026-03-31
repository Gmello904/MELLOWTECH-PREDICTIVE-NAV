import streamlit as st
import pandas as pd
import numpy as np
import pytz
from datetime import datetime as dt
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# LOADING SCREEN
# ------------------------------------------------
with st.spinner("Launching MELLOWTECH AI Engine..."):
    time.sleep(1)

# ------------------------------------------------
# PREMIUM STYLE
# ------------------------------------------------
st.markdown("""
<style>

/* ---------------- APP BACKGROUND ---------------- */
.stApp{
    background:linear-gradient(135deg,#020617,#0f172a);
    color:white;
}

/* ---------------- REMOVE BRANDING ---------------- */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

/* KEEP HEADER FOR SIDEBAR SLIDE BUTTON */
header{
    background:transparent;
}

/* ---------------- SIDEBAR ---------------- */
[data-testid="stSidebar"]{
    background:#020617;
    border-right:1px solid #1e293b;
}

/* Sidebar title */
.sidebar-title{
    font-size:22px;
    font-weight:700;
    margin-bottom:15px;
    color:white;
}

/* Radio buttons style */
div[role="radiogroup"] > label{
    padding:12px;
    border-radius:10px;
    margin-bottom:6px;
    color:silver;
    font-size:16px;
}

div[role="radiogroup"] > label:hover{
    background:#0f172a;
    color:white;
}

/* Active page */
div[role="radiogroup"] > label[data-selected="true"]{
    background:#111827;
    color:#00cfff;
    border-left:4px solid #00cfff;
}

/* Title Glow */
.title{
    text-align:center;
    font-size:48px;
    font-weight:900;
    color:#00ffff;
    text-shadow:
        0 0 10px #00ffff,
        0 0 20px #00ffff;
}

/* Metric color */
[data-testid="stMetricValue"]{
    color:#00cfff;
}

/* Smooth page animation */
section.main > div{
    animation:fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn{
    from{opacity:0;transform:translateY(10px);}
    to{opacity:1;transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR WITH ICONS
# ------------------------------------------------
st.sidebar.markdown(
    "<div class='sidebar-title'>MELLOWTECH</div>",
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "🚦 Traffic",
        "🧭 Navigation",
        "📊 Analytics",
        "👤 Profile"
    ]
)

# ------------------------------------------------
# DASHBOARD PAGE
# ------------------------------------------------
if menu == "🏠 Dashboard":

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.title("Smart Mobility Dashboard")

    timezone = pytz.timezone("Africa/Johannesburg")
    current_time = dt.now(timezone).strftime("%H:%M:%S")

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Time", current_time)
    col2.metric("System Status", "Online")
    col3.metric("AI Engine", "Active")

    st.success("🟢 Predictive Traffic Intelligence Running")

# ------------------------------------------------
# TRAFFIC PAGE
# ------------------------------------------------
elif menu == "🚦 Traffic":

    st.title("Traffic Prediction")

    locations = ["Home", "Work", "School", "Mall"]

    start = st.selectbox("Start", locations)
    end = st.selectbox("Destination", locations)
    leave_time = st.slider("Departure Time", 6, 22, 8)

    np.random.seed(leave_time)

    base = np.random.randint(10, 80, len(locations))

    congestion = [
        c + 20 if 7 <= leave_time <= 9 or 16 <= leave_time <= 18 else c
        for c in base
    ]

    congestion = [min(100, c) for c in congestion]

    df = pd.DataFrame({
        "Location": locations,
        "Congestion %": congestion
    })

    st.dataframe(df, use_container_width=True)

    st.subheader("Traffic Lights")

    for i in range(len(df)):
        level = df.loc[i, "Congestion %"]
        icon = "🔴" if level > 60 else "🔵"
        status = "High Traffic" if level > 60 else "Low Traffic"
        st.write(f"{icon} {df.loc[i,'Location']} — {status}")

    st.line_chart(df.set_index("Location"))

    best = df.loc[df["Congestion %"].idxmin(), "Location"]
    st.success(f"Best Location to Start From: {best}")

# ------------------------------------------------
# NAVIGATION PAGE
# ------------------------------------------------
elif menu == "🧭 Navigation":

    st.title("Live Navigation")

    map_data = pd.DataFrame({
        "lat": [-25.7461, -25.7580],
        "lon": [28.1881, 28.1890]
    })

    st.map(map_data)

# ------------------------------------------------
# ANALYTICS PAGE
# ------------------------------------------------
elif menu == "📊 Analytics":

    st.title("Traffic Analytics")

    data = pd.DataFrame({
        "Average Speed (km/h)": [60,55,70,50,65],
        "Traffic Flow (cars/min)": [40,50,35,55,45],
        "Congestion Level (%)": [20,35,10,50,25]
    },
    index=["Home","Work","School","Mall","Station"])

    st.table(data)
    st.bar_chart(data)

# ------------------------------------------------
# PROFILE PAGE
# ------------------------------------------------
elif menu == "👤 Profile":

    st.title("User Profile")
    st.write("Welcome to MELLOWTECH Dashboard.")
