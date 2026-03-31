import streamlit as st
import pandas as pd
import numpy as np
import pytz
from datetime import datetime as dt
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# BEAUTIFUL THEME (BLUE + RED)
# -----------------------------
st.markdown("""
<style>
body {
    background-color:#0f172a;
}
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
}
[data-testid="stSidebar"]{
    background:#020617;
    border-right:2px solid #00cfff;
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
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR MENU WITH ICONS
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="MELLOWTECH",
        options=["Dashboard","Traffic","Navigation","Analytics","Profile"],
        icons=["speedometer","car-front","map","bar-chart","person-circle"],  # real icons
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#020617"},
            "icon": {"color": "#00cfff", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#ff0033"},
            "nav-link-selected": {"background-color": "#00cfff"},
        }
    )

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if selected == "Dashboard":
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
elif selected == "Traffic":
    st.title("Traffic Prediction")

    locations = ["Home","Work","School","Mall"]
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
elif selected == "Navigation":
    st.title("Live Navigation")

    map_data = pd.DataFrame({
        "lat": [-25.7461, -25.7580],
        "lon": [28.1881, 28.1890]
    })

    st.map(map_data)

# -----------------------------
# ANALYTICS PAGE (EASY VERSION)
# -----------------------------
elif selected == "Analytics":
    st.title("Traffic Analytics - Quick Overview")

    st.markdown("**Here’s a simple view of traffic speed, flow, and density.**")

    data = pd.DataFrame(
        np.random.randint(30, 100, size=(10,3)),  # simplified data
        columns=["Speed (km/h)", "Flow (cars/min)", "Density (cars/km)"]
    )

    st.table(data)  # easy-to-read table
    st.bar_chart(data)  # simple bar chart

    st.info("Quick insights help users plan their travel faster.")

# -----------------------------
# PROFILE PAGE
# -----------------------------
elif selected == "Profile":
    st.title("User Profile")
    st.write("Welcome to MELLOWTECH Dashboard!")
    st.info("Explore Dashboard, Traffic, Navigation, and Analytics easily with icons.")
