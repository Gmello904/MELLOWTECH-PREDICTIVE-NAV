import streamlit as st
import pandas as pd
import numpy as np
import pytz
from datetime import datetime as dt

# ------------------------------------------------
# PAGE CONFIG (IMPORTANT FOR PHONE)
# ------------------------------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="collapsed"   # ⭐ collapsed by default on phone
)

# ------------------------------------------------
# MOBILE + PREMIUM STYLE
# ------------------------------------------------
st.markdown("""
<style>

/* APP BACKGROUND */
.stApp{
    background:linear-gradient(135deg,#020617,#0f172a);
    color:white;
}

/* Remove Streamlit branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header{background:transparent;}

/* SIDEBAR */
[data-testid="stSidebar"]{
    background:#020617;
    border-right:1px solid #1e293b;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px){

    /* make sidebar full height mobile */
    [data-testid="stSidebar"]{
        width:260px !important;
    }

    /* bigger tap buttons */
    div[role="radiogroup"] label{
        font-size:20px;
        padding:18px;
    }
}

/* Menu Style */
div[role="radiogroup"] label{
    padding:14px;
    border-radius:12px;
    color:silver;
    font-size:17px;
    display:block;
}

div[role="radiogroup"] label:hover{
    background:#0f172a;
    color:white;
}

div[role="radiogroup"] label[data-selected="true"]{
    background:#111827;
    color:#00cfff;
    border-left:4px solid #00cfff;
}

/* Glow Title */
.title{
    text-align:center;
    font-size:42px;
    font-weight:900;
    color:#00ffff;
    text-shadow:0 0 15px #00ffff;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# COLLAPSIBLE SIDEBAR MENU
# ------------------------------------------------
st.sidebar.title("MELLOWTECH")

menu = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "🚦 Traffic",
        "🧭 Navigation",
        "📊 Analytics",
        "👤 Profile"
    ]
)

# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------
if menu == "🏠 Dashboard":

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)

    timezone = pytz.timezone("Africa/Johannesburg")
    time_now = dt.now(timezone).strftime("%H:%M:%S")

    c1, c2, c3 = st.columns(3)

    c1.metric("Time", time_now)
    c2.metric("System", "Online")
    c3.metric("AI Engine", "Active")

    st.success("Predictive Traffic Intelligence Running")

# ------------------------------------------------
# TRAFFIC
# ------------------------------------------------
elif menu == "🚦 Traffic":

    st.title("Traffic Prediction")

    locations = ["Home","Work","School","Mall"]

    start = st.selectbox("Start", locations)
    end = st.selectbox("Destination", locations)
    leave = st.slider("Departure",6,22,8)

    np.random.seed(leave)
    congestion = np.random.randint(20,90,len(locations))

    df = pd.DataFrame({
        "Location":locations,
        "Congestion %":congestion
    })

    st.dataframe(df,use_container_width=True)
    st.line_chart(df.set_index("Location"))

# ------------------------------------------------
# NAVIGATION
# ------------------------------------------------
elif menu == "🧭 Navigation":

    st.title("Live Navigation")

    map_data = pd.DataFrame({
        "lat":[-25.7461,-25.7580],
        "lon":[28.1881,28.1890]
    })

    st.map(map_data)

# ------------------------------------------------
# ANALYTICS
# ------------------------------------------------
elif menu == "📊 Analytics":

    st.title("Traffic Analytics")

    data = pd.DataFrame({
        "Speed":[60,55,70,50,65],
        "Flow":[40,50,35,55,45],
        "Congestion":[20,35,10,50,25]
    })

    st.bar_chart(data)

# ------------------------------------------------
# PROFILE
# ------------------------------------------------
elif menu == "👤 Profile":

    st.title("User Profile")
    st.write("Welcome to MELLOWTECH.")
