import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pytz
from datetime import datetime as dt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide"
)

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = {}

if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
body {background:#121212;color:white;}
.block-container{
    background:#1e1e1e;
    border-radius:12px;
    padding:2rem;
}
.title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#00f0ff;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Login Page
# -----------------------------
def login_page():
    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
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

    st.markdown("### OR")
    if st.button("Continue with Google"):
        st.session_state.user = "google_user@gmail.com"
        st.session_state.page = "dashboard"
        st.rerun()

# -----------------------------
# Signup Page
# -----------------------------
def signup_page():
    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
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

# -----------------------------
# Dashboard and Pages
# -----------------------------
def dashboard():
    st.sidebar.success(f"Logged in as {st.session_state.user}")

    menu = st.sidebar.radio(
        "Menu",
        ["Dashboard","Predict Traffic","Map","Reports","Profile"]
    )

    if menu == "Dashboard":
        st.header("MELLOWTECH Dashboard")
        timezone = pytz.timezone("Africa/Johannesburg")
        current_time = dt.now(timezone).strftime("%H:%M:%S")
        st.metric("Current Time", current_time)
        st.success("Traffic Intelligence Online")

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

    if menu == "Map":
        st.header("Navigation Map")
        map_data = pd.DataFrame({
            "lat":[-25.7461,-25.7580],
            "lon":[28.1881,28.1890]
        })
        st.map(map_data)

    if menu == "Reports":
        issue = st.selectbox("Report Issue", ["Accident","Traffic Jam","Roadblock"])
        if st.button("Submit"):
            st.success("Report Sent")

    if menu == "Profile":
        st.write("User:", st.session_state.user)
        if st.button("Logout"):
            st.session_state.page = "login"
            st.session_state.user = None
            st.rerun()

# -----------------------------
# Page routing
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "dashboard":
    dashboard()
