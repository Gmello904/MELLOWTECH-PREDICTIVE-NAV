import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------
# LOADING SCREEN
# ------------------------------------------------
with st.spinner("Launching MELLOWTECH AI Engine..."):
    time.sleep(1)

# ------------------------------------------------
# PREMIUM STYLE
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

    [data-testid="stSidebar"]{
        width:260px !important;
    }

    div[role="radiogroup"] label{
        font-size:20px;
        padding:18px;
    }
}

/* Sidebar radio buttons */
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
# DASHBOARD PAGE
# ------------------------------------------------
if menu == "🏠 Dashboard":

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)

    # FIXED TIME (NO PYTZ REQUIRED)
    time_now = dt.now().strftime("%H:%M:%S")

    c1, c2, c3 = st.columns(3)
    c1.metric("Time", time_now)
    c2.metric("System", "Online")
    c3.metric("AI Engine", "Active")

    st.success("Predictive Traffic Intelligence Running")

# ------------------------------------------------
# TRAFFIC PAGE
# ------------------------------------------------
elif menu == "🚦 Traffic":

    st.title("Traffic Prediction")

    locations = ["Home","Work","School","Mall"]

    start = st.selectbox("Start", locations)
    end = st.selectbox("Destination", locations)
    leave = st.slider("Departure Time",6,22,8)

    # AI Simulation
    np.random.seed(leave)
    base = np.random.randint(10,80,len(locations))

    congestion = [
        c + 25 if 7 <= leave <= 9 or 16 <= leave <= 18 else c
        for c in base
    ]

    congestion = [min(100,c) for c in congestion]

    df = pd.DataFrame({
        "Location":locations,
        "Congestion %":congestion
    })

    st.dataframe(df,use_container_width=True)

    st.subheader("AI Traffic Lights")

    for i in range(len(df)):
        level = df.loc[i,"Congestion %"]

        if level > 65:
            light = "🔴"
            status = "Heavy Traffic"
        else:
            light = "🔵"
            status = "Smooth Flow"

        st.markdown(f"### {light} {df.loc[i,'Location']} — {status}")

    st.line_chart(df.set_index("Location"))

    best = df.loc[df["Congestion %"].idxmin(),"Location"]
    st.success(f"✅ Recommended Route Start: {best}")

# ------------------------------------------------
# NAVIGATION PAGE
# ------------------------------------------------
elif menu == "🧭 Navigation":

    st.title("Live Navigation")

    map_data = pd.DataFrame({
        "lat":[-25.7461,-25.7580],
        "lon":[28.1881,28.1890]
    })

    st.map(map_data)

# ------------------------------------------------
# ANALYTICS PAGE
# ------------------------------------------------
elif menu == "📊 Analytics":

    st.title("Traffic Analytics")

    data = pd.DataFrame({
        "Speed":[60,55,70,50,65],
        "Flow":[40,50,35,55,45],
        "Congestion":[20,35,10,50,25]
    })

    st.table(data)
    st.bar_chart(data)

# ------------------------------------------------
# PROFILE PAGE
# ------------------------------------------------
elif menu == "👤 Profile":

    st.title("User Profile")
    st.write("Welcome to MELLOWTECH Dashboard.")
