import streamlit as st
import pandas as pd
import numpy as np
import pytz
from datetime import datetime as dt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# THEME + STYLES
# -----------------------------
st.markdown("""
<style>
body { background-color:#0f172a; }
.stApp { background: linear-gradient(135deg,#020617,#0f172a); }

[data-testid="stSidebar"]{
    background:#020617;
    border-right:2px solid #00cfff;
    padding-top:20px;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:800;
    color:#00cfff;
}

/* ✅ FIXED EQUAL BUTTONS */
.stButton>button{
    width:100%;
    height:65px;              /* SAME HEIGHT */
    border-radius:12px;
    background:linear-gradient(90deg,#00cfff,#ff0033);
    color:white;
    font-weight:bold;
    border:none;
    font-size:16px;

    display:flex;
    align-items:center;
    justify-content:flex-start;

    padding-left:20px;
    margin-bottom:12px;       /* SAME SPACING */
}

/* 🔥 HOVER EFFECT */
.stButton>button:hover{
    transform:scale(1.03);
    box-shadow:0 0 10px #00cfff;
    transition:0.3s;
}

[data-testid="stMetricValue"]{
    color:#00cfff;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("MELLOWTECH")

icons = {
    "Dashboard": "speed",
    "Traffic": "car",
    "Navigation": "map",
    "Analytics": "chart",
    "Profile": "user"
}

menu = None
for page in icons.keys():
    if st.sidebar.button(page):
        menu = page

# Default
if menu is None:
    menu = "Dashboard"

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":
    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.title("Smart Mobility Dashboard")

    timezone = pytz.timezone("Africa/Johannesburg")
    current_time = dt.now(timezone).strftime("%H:%M:%S")

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Time", current_time)
    col2.metric("System Status", "Online")
    col3.metric("AI Engine", "Active")

    st.success("Predictive Traffic Intelligence Running")

# -----------------------------
# TRAFFIC
# -----------------------------
elif menu == "Traffic":
    st.title("Traffic Prediction")

    locations = ["Home", "Work", "School", "Mall"]
    start = st.selectbox("Start", locations)
    end = st.selectbox("Destination", locations)
    leave_time = st.slider("Departure Time", 6, 22, 8)

    np.random.seed(1)
    congestion = np.random.randint(10, 90, 5)

    df = pd.DataFrame({
        "Hour": [leave_time + i for i in range(5)],
        "Congestion %": congestion
    })

    st.dataframe(df, use_container_width=True)

    st.line_chart(df.set_index("Hour"))

    # Indicator
    df["Level"] = df["Congestion %"].apply(
        lambda x: "🔴 High" if x > 60 else "🔵 Low"
    )

    st.table(df[["Hour", "Congestion %", "Level"]])

    best = df.loc[df["Congestion %"].idxmin(), "Hour"]
    st.success(f"Best Time To Leave: {best}:00")

# -----------------------------
# NAVIGATION
# -----------------------------
elif menu == "Navigation":
    st.title("Live Navigation")

    map_data = pd.DataFrame({
        "lat": [-25.7461, -25.7580],
        "lon": [28.1881, 28.1890]
    })

    st.map(map_data)

# -----------------------------
# ANALYTICS
# -----------------------------
elif menu == "Analytics":
    st.title("Traffic Analytics")
    st.markdown("**Quick overview of key traffic data for easy decisions.**")

    data = pd.DataFrame({
        "Average Speed (km/h)": [60, 55, 70, 50, 65],
        "Traffic Flow (cars/min)": [40, 50, 35, 55, 45],
        "Congestion Level (%)": [20, 35, 10, 50, 25]
    }, index=["Home", "Work", "School", "Mall", "Station"])

    st.table(data)
    st.bar_chart(data)

    st.info("View traffic metrics quickly for smarter travel planning.")

# -----------------------------
# PROFILE
# -----------------------------
elif menu == "Profile":
    st.title("User Profile")
    st.write("Welcome to MELLOWTECH Dashboard!")
    st.info("Explore Dashboard, Traffic, Navigation, and Analytics easily using the sidebar.")
