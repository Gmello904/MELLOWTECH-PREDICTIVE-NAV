# MELLOETECH PREDICTIVE NAVIGATION APP

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pytz
from datetime import datetime as dt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MELLOETECH",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = {}

if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# CSS STYLING
# -----------------------------
st.markdown("""
<style>
/* Hide default Streamlit header/footer */
header, #MainMenu, footer {visibility: hidden;}

/* General body */
body {background:#121212;color:white;font-family:Helvetica, sans-serif;}

/* Card container */
.block-container{
    background:#1e1e1e;
    border-radius:12px;
    padding:2rem;
    max-width:900px;
    margin:auto;
}

/* Title styling */
.title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#00f0ff;
    margin-bottom:1rem;
}

/* Buttons */
.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-weight: 600;
}

/* Table headers */
.css-1v3fvcr th {
    color: #00f0ff !important;
}

/* Line chart */
.css-10trblm {
    background-color: #1e1e1e;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    st.markdown("<div class='title'>MELLOETECH</div>", unsafe_allow_html=True)
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in st.session_state.users and st.session_state.users[email] == password:
            st.session_state.user = email
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid login")

    st.divider()

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SIGNUP PAGE
# -----------------------------
def signup_page():
    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    st.markdown("<div class='title'>MELLOETECH</div>", unsafe_allow_html=True)
    st.subheader("Create Account")

    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if new_email and new_password:
            st.session_state.users[new_email] = new_password
            st.success("Account created!")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# DASHBOARD AND PAGES
# -----------------------------
def dashboard():
    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    st.sidebar.success(f"Logged in as {st.session_state.user}")

    menu = st.sidebar.radio(
        "Menu",
        ["Dashboard","Predict Traffic","Map","Reports","Profile"]
    )

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    if menu == "Dashboard":
        st.header("MELLOETECH Dashboard")
        timezone = pytz.timezone("Africa/Johannesburg")
        current_time = dt.now(timezone).strftime("%H:%M:%S")
        st.metric("Current Time", current_time)
        st.success("Traffic Intelligence Online")

    # -----------------------------
    # PREDICT TRAFFIC
    # -----------------------------
    if menu == "Predict Traffic":
        locations = ["Home","Work","School","Mall"]
        start = st.selectbox("Start", locations)
        end = st.selectbox("Destination", locations)
        leave_time = st.slider("Leave Time",6,22,8)

        np.random.seed(1)
        congestion = np.random.randint(10,90,3)
        df = pd.DataFrame({
            "Hour":[leave_time+i for i in range(3)],
            "Congestion %":congestion
        })

        st.table(df)
        st.line_chart(df.set_index("Hour"))
        best_time = df.loc[df["Congestion %"].idxmin(),"Hour"]
        st.success(f"Best departure time: {best_time}:00")

    # -----------------------------
    # MAP PAGE
    # -----------------------------
    if menu == "Map":
        st.header("Navigation Map")
        map_data = pd.DataFrame({
            "lat":[-25.7461,-25.7580],
            "lon":[28.1881,28.1890]
        })
        st.map(map_data)

    # -----------------------------
    # REPORTS PAGE
    # -----------------------------
    if menu == "Reports":
        issue = st.selectbox("Report Issue", ["Accident","Traffic Jam","Roadblock"])
        if st.button("Submit"):
            st.success("Report Sent")

    # -----------------------------
    # PROFILE PAGE
    # -----------------------------
    if menu == "Profile":
        st.write("User:", st.session_state.user)
        if st.button("Logout"):
            st.session_state.page = "login"
            st.session_state.user = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# PAGE ROUTING
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "dashboard":
    dashboard()
