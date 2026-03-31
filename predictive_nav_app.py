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

.stButton>button{
    width:100%;
    border-radius:10px;
    background:linear-gradient(90deg,#00cfff,#ff0033);
    color:white;
    font-weight:bold;
    border:none;
}

[data-testid="stMetricValue"]{
    color:#00cfff;
}

.sidebar-icon {
    width:30px;
    height:30px;
    margin-right:10px;
    filter: brightness(0.8) invert(0.8); /* makes it silver */
}
.sidebar-button {
    display:flex;
    align-items:center;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD ICONS (using URLs or local paths)
# You can replace these with your own SVG/PNG files
# -----------------------------
icons = {
    "Dashboard": "https://img.icons8.com/ios-filled/50/ffffff/speed.png",
    "Traffic": "https://img.icons8.com/ios-filled/50/ffffff/car.png",
    "Navigation": "https://img.icons8.com/ios-filled/50/ffffff/map.png",
    "Analytics": "https://img.icons8.com/ios-filled/50/ffffff/combo-chart.png",
    "Profile": "https://img.icons8.com/ios-filled/50/ffffff/user.png"
}

# -----------------------------
# SIDEBAR NAVIGATION WITH ICONS
# -----------------------------
st.sidebar.title("MELLOWTECH")

menu = None
for page, icon_url in icons.items():
    if st.sidebar.button(f"{page}", key=page):
        menu = page

# Default to Dashboard if nothing clicked
if menu is None:
    menu = "Dashboard"

# -----------------------------
# DASHBOARD PAGE
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
# TRAFFIC PAGE
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

    best = df.loc[df["Congestion %"].idxmin(), "Hour"]
    st.success(f"Best Time To Leave: {best}:00")

# -----------------------------
# NAVIGATION PAGE
# -----------------------------
elif menu == "Navigation":
    st.title("Live Navigation")
    map_data = pd.DataFrame({
        "lat": [-25.7461, -25.7580],
        "lon": [28.1881, 28.1890]
    })
    st.map(map_data)

# -----------------------------
# ANALYTICS PAGE
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
# PROFILE PAGE
# -----------------------------
elif menu == "Profile":
    st.title("User Profile")
    st.write("Welcome to MELLOWTECH Dashboard!")
    st.info("Explore Dashboard, Traffic, Navigation, and Analytics easily using the sidebar.")   I SAID THOSE BOXES SHOLD BE EQUAL AND IN THIS SIZE
