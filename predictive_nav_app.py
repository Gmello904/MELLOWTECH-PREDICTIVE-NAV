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
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "users" not in st.session_state:
    st.session_state.users = {}

if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# IMPROVED UI
# -----------------------------
st.markdown("""
<style>

/* REMOVE STREAMLIT DEFAULT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* GLOBAL WIDTH CONTROL (IMPORTANT FIX) */
.block-container {
    max-width: 1100px;
    padding-left: 4rem;
    padding-right: 4rem;
}

/* Background */
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#020617;
    border-right:2px solid #00cfff;
}

/* TITLE (SHINE EFFECT) */
.title{
    text-align:center;
    font-size:44px;
    font-weight:900;
    color:#00cfff;
    text-shadow:0px 0px 10px #00cfff, 0px 0px 20px #00cfff;
}

/* LOGIN CARD (CENTER + SLIM) */
.card{
    background:#020617;
    padding:30px;
    border-radius:18px;
    max-width:320px;
    margin:60px auto;
    box-shadow:0px 0px 25px rgba(0,207,255,0.3);
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

/* SOCIAL BUTTONS */
.social-btn{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
    padding:10px;
    margin-top:10px;
    border-radius:10px;
    background:#0f172a;
    border:1px solid #00cfff;
    color:white;
    cursor:pointer;
}

/* ICON SIZE */
.icon{
    width:18px;
    height:18px;
}

/* Metrics */
[data-testid="stMetricValue"]{
    color:#00cfff;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

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

    st.markdown("### Or login with", unsafe_allow_html=True)

    # GOOGLE
    st.markdown("""
    <div class='social-btn'>
        <img class='icon' src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg'>
        Google
    </div>
    """, unsafe_allow_html=True)

    # APPLE
    st.markdown("""
    <div class='social-btn'>
        <img class='icon' src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apple/apple-original.svg'>
        Apple
    </div>
    """, unsafe_allow_html=True)

    # PHONE
    st.markdown("""
    <div class='social-btn'>
        <img class='icon' src='https://cdn-icons-png.flaticon.com/512/597/597177.png'>
        Phone Number
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# SIGNUP PAGE
# -----------------------------
def signup_page():

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Create Account")

    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if new_email and new_password:
            st.session_state.users[new_email] = new_password
            st.success("Account Created ✅")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard():

    st.sidebar.title("MELLOWTECH")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard","Traffic","Navigation","Analytics","Profile"]
    )

    st.sidebar.success(f"User: {st.session_state.user}")

    if menu == "Dashboard":

        st.title("Smart Mobility Dashboard")

        timezone = pytz.timezone("Africa/Johannesburg")
        current_time = dt.now(timezone).strftime("%H:%M:%S")

        col1,col2,col3 = st.columns(3)

        col1.metric("Current Time", current_time)
        col2.metric("System Status","Online")
        col3.metric("AI Engine","Active")

        st.success("MELLOWTECH Predictive Traffic Intelligence Running")

    elif menu == "Traffic":

        st.title("Traffic Prediction")

        locations = ["Home","Work","School","Mall"]

        start = st.selectbox("Start",locations)
        end = st.selectbox("Destination",locations)
        leave_time = st.slider("Departure Time",6,22,8)

        np.random.seed(1)

        congestion = np.random.randint(10,90,5)

        df = pd.DataFrame({
            "Hour":[leave_time+i for i in range(5)],
            "Congestion %":congestion
        })

        st.dataframe(df,use_container_width=True)
        st.line_chart(df.set_index("Hour"))

        best = df.loc[df["Congestion %"].idxmin(),"Hour"]

        st.success(f"Best Time To Leave: {best}:00")

    elif menu == "Navigation":

        st.title("Live Navigation")

        map_data = pd.DataFrame({
            "lat":[-25.7461,-25.7580],
            "lon":[28.1881,28.1890]
        })

        st.map(map_data)

    elif menu == "Analytics":

        st.title("Traffic Analytics")

        data = pd.DataFrame(
            np.random.randn(50,3),
            columns=["Speed","Flow","Density"]
        )

        st.area_chart(data)

        st.info("AI analysing traffic patterns across Gauteng.")

    elif menu == "Profile":

        st.title("User Profile")

        st.write("Logged in as:",st.session_state.user)

        if st.button("Logout"):
            st.session_state.user=None
            st.session_state.page="login"
            st.rerun()


# -----------------------------
# ROUTING
# -----------------------------
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "signup":
    signup_page()

elif st.session_state.page == "dashboard":
    dashboard()
