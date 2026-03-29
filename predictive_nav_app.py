# =====================================================
# MELLOWTECH PREDICTIVE NAVIGATION APP (FULL VERSION)
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
import pytz
from datetime import datetime as dt

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="MELLOWTECH Navigation",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon=None
)

# =====================================================
# DARK RESPONSIVE STYLE
# =====================================================
st.markdown("""
<style>
/* Hide Streamlit branding and toolbar */
header, #MainMenu, footer, [data-testid="stToolbar"] {display:none !important;}

/* General background and font */
body {background-color:#121212; color:white; font-family:'Helvetica', sans-serif;}

/* Main container card */
.block-container {
    background:#1e1e1e; padding:2rem; border-radius:15px; max-width:1000px; margin:auto;
}

/* Login/Signup card */
.login-card {
    background:#2a2a2a; padding:2rem; border-radius:1rem; max-width:450px; margin:auto; text-align:center;
}

/* Title style */
#title{
    font-size:2.5rem; font-weight:900; color:#00f0ff; text-shadow:0 0 10px #00f0ff; margin-bottom:20px;
}

/* Section card */
.section {
    background:#2a2a2a; padding:1rem 1.5rem; border-radius:0.8rem; margin-bottom:1rem;
}

/* Buttons */
.stButton>button{
    background-color:#1f77b4 !important; color:white !important; border-radius:0.5rem; padding:0.5rem 1rem; font-weight:600;
}

/* Input text color */
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stSlider>div>div>div{
    color:#e0e0e0 !important;
}

/* Responsive adjustments */
@media (max-width: 768px){
    #title{font-size:2rem;}
    .block-container{padding:1rem;}
    .login-card{padding:1.5rem;}
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOGIN/SIGNUP SYSTEM
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {}  # store accounts temporarily
if "page" not in st.session_state:
    st.session_state.page = "login"

def login_page():
    st.markdown("<div id='title'>MELLOWTECH Navigation</div>", unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in st.session_state.users and st.session_state.users[email]==password:
            st.session_state.logged_in=True
            st.session_state.user=email
            st.session_state.page="dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials or account does not exist")

    st.markdown("### OR")
    if st.button("Create Account"):
        st.session_state.page="signup"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    st.markdown("<div id='title'>Create Account</div>", unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if new_email and new_password:
            st.session_state.users[new_email] = new_password
            st.success("Account created! Please login.")
            st.session_state.page="login"
            st.rerun()
        else:
            st.error("Enter email and password")

    if st.button("Back to Login"):
        st.session_state.page="login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# LOGIN PAGE ROUTING
# =====================================================
if not st.session_state.logged_in:
    if st.session_state.page=="login":
        login_page()
    elif st.session_state.page=="signup":
        signup_page()
    st.stop()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard","Predict Traffic","Navigation Map","Reports","Profile"]
)

# =====================================================
# SIMULATED TRAFFIC DATA
# =====================================================
np.random.seed(42)
locations = ["Home","Work","School","Gym","Mall"]
hours = np.arange(6,22)
traffic_matrix = pd.DataFrame(np.random.rand(len(locations),len(hours)), index=locations, columns=hours)
coords = {"Home":(-25.7461,28.1881),"Work":(-25.7580,28.1890),"School":(-25.7500,28.2000),"Gym":(-25.7400,28.1800),"Mall":(-25.7450,28.1950)}

# =====================================================
# WEATHER FUNCTION
# =====================================================
def get_weather(lat,lon):
    url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data=requests.get(url).json()
    cw=data["current_weather"]
    return {"temperature":cw["temperature"], "windspeed":cw["windspeed"], "winddir":cw["winddirection"], "code":cw["weathercode"]}

weather_map={0:"Clear",2:"Partly Cloudy",3:"Overcast",45:"Fog",61:"Rain",63:"Moderate Rain",65:"Heavy Rain",95:"Thunderstorm"}

# =====================================================
# DASHBOARD PAGE
# =====================================================
if menu=="Dashboard":
    st.markdown("<div id='title'>MELLOWTECH Dashboard</div>", unsafe_allow_html=True)
    timezone=pytz.timezone("Africa/Johannesburg")
    current_time=dt.now(timezone).strftime("%H:%M:%S")
    st.metric("Current Time",current_time)
    st.success(f"Logged in as {st.session_state.user}")
    st.info("AI Mobility Intelligence Active")

# =====================================================
# PREDICT TRAFFIC PAGE
# =====================================================
if menu=="Predict Traffic":
    st.markdown("<div class='section'>Predict Traffic Congestion</div>", unsafe_allow_html=True)
    col1,col2,col3=st.columns(3)
    with col1: start=st.selectbox("Start Location",locations)
    with col2: end=st.selectbox("Destination",locations)
    with col3: commute_day=st.date_input("Date",datetime.date.today())
    preferred_leave_time=st.slider("Preferred Leave Time",6,22,8)
    start_lat,start_lon=coords[start]
    weather=get_weather(start_lat,start_lon)

    with st.container():
        st.markdown("<div class='section'>🌦 Live Weather</div>", unsafe_allow_html=True)
        st.write(f"Temperature: {weather['temperature']}°C")
        st.write(f"Condition: {weather_map.get(weather['code'],'Unknown')}")
        if weather['code'] in [45,61,63,65,95]:
            st.warning("⚠️ Bad weather may slow traffic")
        else:
            st.success("✅ Good travel conditions")

    def predict_congestion(hour):
        base=traffic_matrix.loc[start,hour]
        rush=0.5 if hour in [7,8,17,18] else 0
        bad_weather=0.2 if weather["code"] in [45,61,63,65,95] else 0
        return min(base+rush+bad_weather,1.0)

    forecast_hours=np.arange(preferred_leave_time,preferred_leave_time+3)
    forecast_data={h:predict_congestion(h) for h in forecast_hours}
    forecast_percent={h:round(v*100) for h,v in forecast_data.items()}

    def traffic_label(v):
        if v<30: return "🟢 Light"
        elif v<60: return "🟡 Moderate"
        else: return "🔴 Heavy"

    congestion_df=pd.DataFrame({"Hour":forecast_percent.keys(),"Congestion %":forecast_percent.values(),"Traffic":[traffic_label(v) for v in forecast_percent.values()]})
    st.table(congestion_df)
    st.line_chart(pd.Series(forecast_percent))
    best_time=min(forecast_data,key=forecast_data.get)
    st.success(f"Optimal Departure Time: {best_time}:00")

# =====================================================
# NAVIGATION MAP PAGE
# =====================================================
if menu=="Navigation Map":
    st.header("Live Navigation Map")
    start,end="Home","Work"
    map_data=pd.DataFrame({"lat":[coords[start][0],coords[end][0]],"lon":[coords[start][1],coords[end][1]]})
    st.map(map_data,zoom=14)

# =====================================================
# REPORTS PAGE
# =====================================================
if menu=="Reports":
    st.header("Report Road Issue")
    issue=st.selectbox("Issue Type",["Accident","Traffic Jam","Roadblock","Pothole"])
    if st.button("Submit Report"):
        st.success("Report submitted!")

# =====================================================
# PROFILE PAGE
# =====================================================
if menu=="Profile":
    st.header("User Profile")
    st.write(f"Logged in as: {st.session_state.user}")
    st.text_input("Home Location")
    st.text_input("Work Location")
    if st.button("Logout"):
        st.session_state.logged_in=False
        st.session_state.user=None
        st.rerun()
