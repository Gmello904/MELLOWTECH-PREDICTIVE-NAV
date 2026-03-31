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
# UPDATED THEME (BLACK + WHITE + ANIMATION)
# -----------------------------
st.markdown("""
<style>

/* Hide Streamlit default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(135deg,#000000,#111111);
    animation: fadeIn 1s ease-in-out;
}

/* Fade animation */
@keyframes fadeIn {
    from {opacity:0; transform:translateY(20px);}
    to {opacity:1; transform:translateY(0);}
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#000;
    border-right:1px solid #fff;
}

/* Titles */
.title{
    text-align:center;
    font-size:42px;
    font-weight:800;
    color:#ffffff;
}

/* Login Card (THINNER) */
.card{
    background:#000;
    padding:30px;
    border-radius:14px;
    max-width:320px;
    margin:auto;
    border:1px solid #fff;
    animation: slideUp 0.8s ease;
}

/* Card animation */
@keyframes slideUp {
    from {opacity:0; transform:translateY(40px);}
    to {opacity:1; transform:translateY(0);}
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:8px;
    background:white;
    color:black;
    font-weight:bold;
    border:none;
    transition:0.3s;
}

.stButton>button:hover{
    background:black;
    color:white;
    border:1px solid white;
}

/* Inputs */
input{
    background:black !important;
    color:white !important;
    border:1px solid white !important;
}

/* Toggle container */
.toggle-container{
    display:flex;
    justify-content:center;
    margin-bottom:15px;
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

    # Toggle Switch (UI only)
    st.markdown("<div class='toggle-container'>", unsafe_allow_html=True)
    mode = st.toggle("Dark / Light Mode")
    st.markdown("</div>", unsafe_allow_html=True)

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
# DASHBOARD APP
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
