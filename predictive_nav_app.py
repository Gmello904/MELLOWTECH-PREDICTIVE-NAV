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
# THEME + STYLES (Glowing Title & Equal Rect Buttons)
# -----------------------------
st.markdown("""
<style>
body { background-color:#0f172a; }
.stApp { background: linear-gradient(135deg,#020617,#0f172a); }

/* Sidebar */
[data-testid="stSidebar"]{
    background:#020617;
    border-right:2px solid #00cfff;
    padding-top:20px;
}

/* Sidebar buttons as equal rectangles */
.stButton>button {
    width: 100%;
    height: 70px;
    border-radius: 12px;
    background: linear-gradient(90deg,#00cfff,#ff0033);
    color: white;
    font-weight: bold;
    font-size: 18px;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    box-sizing: border-box;
}

/* Hover effect */
.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px #00cfff, 0 0 30px #ff0033;
    transition: 0.2s;
}

/* Glowing title */
.title{
    text-align:center;
    font-size:48px;
    font-weight:900;
    color:#00ffff;
    text-shadow:
        0 0 5px #00ffff,
        0 0 10px #00ffff,
        0 0 20px #00ffff,
        0 0 40px #00ffff,
        0 0 80px #00ffff;
}

/* Metric color */
[data-testid="stMetricValue"]{
    color:#00cfff;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("MELLOWTECH")

pages = ["Dashboard", "Traffic", "Navigation", "Analytics", "Profile"]

menu = None
for page in pages:
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

    # Simulate congestion dynamically based on departure time
    np.random.seed(leave_time)  # dynamic results
    base_congestion = np.random.randint(10, 80, len(locations))
    congestion = [c + 20 if 7 <= leave_time <= 9 or 16 <= leave_time <= 18 else c for c in base_congestion]
    congestion = [min(100, c) for c in congestion]  # cap at 100%

    df = pd.DataFrame({
        "Location": locations,
        "Congestion %": congestion
    })

    st.dataframe(df, use_container_width=True)

    # 🔴🔵 Traffic light indicator
    st.subheader("Traffic Lights")
    for i in range(len(df)):
        level = df.loc[i, "Congestion %"]
        if level > 60:
            color = "🔴"
            status = "High Traffic"
        else:
            color = "🔵"
            status = "Low Traffic"
        st.markdown(f"**{df.loc[i, 'Location']}** → {color} {status}")

    # Line chart
    st.line_chart(df.set_index("Location"))

    best_location = df.loc[df["Congestion %"].idxmin(), "Location"]
    st.success(f"Best Location to Start From: {best_location}")

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

    data = pd.DataFrame({
        "Average Speed (km/h)": [60, 55, 70, 50, 65],
        "Traffic Flow (cars/min)": [40, 50, 35, 55, 45],
        "Congestion Level (%)": [20, 35, 10, 50, 25]
    }, index=["Home", "Work", "School", "Mall", "Station"])

    st.table(data)
    st.bar_chart(data)

# -----------------------------
# PROFILE
# -----------------------------
elif menu == "Profile":
    st.title("User Profile")
    st.write("Welcome to MELLOWTECH Dashboard!")
