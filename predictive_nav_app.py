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
# BEAUTIFUL THEME (BLUE + RED)
# -----------------------------
st.markdown("""
<style>

/* Background */
body {
    background-color:#0f172a;
}

/* Main App */
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#020617;
    border-right:2px solid #00cfff;
}

/* Titles */
.title{
    text-align:center;
    font-size:42px;
    font-weight:800;
    color:#00cfff;
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:10px;
    background:linear-gradient(90deg,#00cfff,#ff0033);
    color:white;
    font-weight:bold;
    border:none;
}

/* Metrics */
[data-testid="stMetricValue"]{
    color:#00cfff;
}

/* Mobile Responsive */
@media (max-width:768px){
.card{
    margin-top:20px;
}
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# DASHBOARD APP (LEFT SIDEBAR)
# -----------------------------
def dashboard():
    st.sidebar.title("MELLOWTECH")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard","Traffic","Navigation","Analytics","Profile"]
    )

    # ---------------- DASHBOARD
    if menu == "Dashboard":
        st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
        st.title("Smart Mobility Dashboard")

        timezone = pytz.timezone("Africa/Johannesburg")
        current_time = dt.now(timezone).strftime("%H:%M:%S")

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Time", current_time)
        col2.metric("System Status", "Online")
        col3.metric("AI Engine", "Active")

        st.success("MELLOWTECH Predictive Traffic Intelligence Running")

    # ---------------- TRAFFIC
    elif menu == "Traffic":
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

    # ---------------- NAVIGATION
    elif menu == "Navigation":
        st.title("Live Navigation")

        map_data = pd.DataFrame({
            "lat": [-25.7461, -25.7580],
            "lon": [28.1881, 28.1890]
        })

        st.map(map_data)

    # ---------------- ANALYTICS
    elif menu == "Analytics":
        st.title("Traffic Analytics")

        data = pd.DataFrame(
            np.random.randn(50, 3),
            columns=["Speed", "Flow", "Density"]
        )

        st.area_chart(data)
        st.info("AI analysing traffic patterns across Gauteng.")

    # ---------------- PROFILE
    elif menu == "Profile":
        st.title("User Profile")
        st.write("Welcome to MELLOWTECH Dashboard!")
        st.info("Here you can explore traffic, analytics, and navigation features without logging in.")


# -----------------------------
# RUN DASHBOARD DIRECTLY
# -----------------------------
dashboard()
