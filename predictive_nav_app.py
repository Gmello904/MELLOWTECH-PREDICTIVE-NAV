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
    padding:10px 0px;
}

.metric-box{
    background:#020617;
    padding:25px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 25px rgba(0,207,255,0.3);
    margin-bottom:20px;
}

[data-testid="stMetricValue"]{
    color:#00cfff;
}

.traffic-light-red{
    width:25px; height:25px; border-radius:50%; background:red; display:inline-block; margin-right:5px;
}
.traffic-light-blue{
    width:25px; height:25px; border-radius:50%; background:blue; display:inline-block; margin-right:5px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR MENU
# -----------------------------
st.sidebar.title("MELLOWTECH")
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Traffic", "Navigation", "Analytics", "Profile"]
)

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if menu == "Dashboard":
    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.title("Smart Mobility Dashboard")

    timezone = pytz.timezone("Africa/Johannesburg")
    current_time = dt.now(timezone).strftime("%H:%M:%S")

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-box'><h3>Current Time</h3><h2>{current_time}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-box'><h3>System Status</h3><h2>Online</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-box'><h3>AI Engine</h3><h2>Active</h2></div>", unsafe_allow_html=True)

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

    # Show traffic lights for each hour
    st.markdown("### Congestion Levels")
    for i, row in df.iterrows():
        light_color = "traffic-light-red" if row["Congestion %"] > 50 else "traffic-light-blue"
        st.markdown(f"<span class='{light_color}'></span> Hour {row['Hour']}: {row['Congestion %']}%", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='metric-box'><h3>Best Time to Leave</h3><h2>{df.loc[df['Congestion %'].idxmin(), 'Hour']}:00</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-box'><h3>Average Congestion</h3><h2>{int(df['Congestion %'].mean())}%</h2></div>", unsafe_allow_html=True)

    st.line_chart(df.set_index("Hour"))

# -----------------------------
# NAVIGATION PAGE
# -----------------------------
elif menu == "Navigation":
    st.title("Live Navigation")
    map_data = pd.DataFrame({
        "lat": [-25.7461, -25.7580],
        "lon": [28.1881, 28.1890]
    })

    col1, col2 = st.columns(2)
    col1.map(map_data)
    col2.markdown("<div class='metric-box'><h3>Navigation Status</h3><h2>Active</h2></div>", unsafe_allow_html=True)

# -----------------------------
# ANALYTICS PAGE
# -----------------------------
elif menu == "Analytics":
    st.title("Traffic Analytics")
    st.markdown("**Quick glance of key traffic metrics for smarter travel decisions.**")

    data = pd.DataFrame({
        "Average Speed (km/h)": [60, 55, 70, 50, 65],
        "Traffic Flow (cars/min)": [40, 50, 35, 55, 45],
        "Congestion Level (%)": [20, 35, 10, 50, 25]
    }, index=["Home", "Work", "School", "Mall", "Station"])

    col1, col2 = st.columns(2)
    col1.table(data)
    col2.bar_chart(data)

# -----------------------------
# PROFILE PAGE
# -----------------------------
elif menu == "Profile":
    st.title("User Profile")
    col1, col2 = st.columns(2)
    col1.markdown("<div class='metric-box'><h3>Username</h3><h2>Guest</h2></div>", unsafe_allow_html=True)
    col2.markdown("<div class='metric-box'><h3>Status</h3><h2>Active</h2></div>", unsafe_allow_html=True)

    st.info("Explore Dashboard, Traffic, Navigation, and Analytics easily using the sidebar.")
