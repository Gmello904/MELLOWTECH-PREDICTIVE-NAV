import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
import time
import random

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="MellowTech | Smart Emission Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
defaults = {
    "logged_in": False,
    "username": "",
    "home_location": "Home",
    "green_points": 0,
    "total_savings": 0.0,
    "eco_score": 72,
    "loaded": False,
    "trips_today": 0,
    "emission_alerts": 0,
    "weekly_scores": [55, 61, 58, 67, 70, 68, 72],
    "driving_mode": "Normal",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.loaded:
    with st.spinner("Initialising MellowTech AI Emission Intelligence..."):
        time.sleep(1)
    st.session_state.loaded = True

# ------------------------------------------------
# STYLE
# ------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;800;900&family=Share+Tech+Mono&display=swap');

:root {
    --green:   #22c55e;
    --green2:  #4ade80;
    --red:     #ef4444;
    --amber:   #f59e0b;
    --blue:    #38bdf8;
    --bg0:     #030712;
    --bg1:     #0a0f1e;
    --bg2:     #0f1929;
    --border:  #1e293b;
    --text:    #e2e8f0;
    --muted:   #475569;
}

* { font-family: 'Exo 2', sans-serif; }

.stApp {
    background: var(--bg0);
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background: var(--bg1);
    border-right: 1px solid var(--border);
}

div[role="radiogroup"] label {
    padding: 13px 16px;
    border-radius: 10px;
    color: #94a3b8;
    font-size: 15px;
    display: block;
    transition: all 0.2s;
    margin-bottom: 4px;
}
div[role="radiogroup"] label:hover { background: var(--bg2); color: white; }
div[role="radiogroup"] label[data-selected="true"] {
    background: #0d2318;
    color: var(--green2);
    border-left: 3px solid var(--green);
    font-weight: 700;
}

/* TITLE */
.mt-title {
    font-size: 44px;
    font-weight: 900;
    color: var(--green2);
    text-shadow: 0 0 30px #22c55e88, 0 0 60px #22c55e33;
    letter-spacing: 3px;
    text-align: center;
    line-height: 1;
}
.mt-sub {
    text-align: center;
    color: var(--muted);
    font-size: 12px;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 28px;
}

/* CARDS */
.card {
    background: linear-gradient(135deg, var(--bg1), var(--bg2));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--green), transparent);
}
.card-red::before   { background: linear-gradient(90deg, transparent, var(--red), transparent); }
.card-amber::before { background: linear-gradient(90deg, transparent, var(--amber), transparent); }
.card-blue::before  { background: linear-gradient(90deg, transparent, var(--blue), transparent); }

.kv { font-size: 34px; font-weight: 900; font-family: 'Share Tech Mono', monospace; }
.kv-green  { color: var(--green2); text-shadow: 0 0 15px #22c55e66; }
.kv-red    { color: var(--red);    text-shadow: 0 0 15px #ef444466; }
.kv-amber  { color: var(--amber);  text-shadow: 0 0 15px #f59e0b66; }
.kv-blue   { color: var(--blue);   text-shadow: 0 0 15px #38bdf866; }
.kl { font-size: 11px; letter-spacing: 3px; color: var(--muted); text-transform: uppercase; margin-top: 4px; }

/* ALERT BOXES */
.alert-red {
    background: #1c0a0a;
    border: 1px solid #7f1d1d;
    border-left: 4px solid var(--red);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
    animation: pulse-red 2s infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 #ef444400; }
    50%       { box-shadow: 0 0 12px 2px #ef444433; }
}
.alert-green {
    background: #071a0e;
    border: 1px solid #14532d;
    border-left: 4px solid var(--green);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
}
.alert-amber {
    background: #1a1203;
    border: 1px solid #78350f;
    border-left: 4px solid var(--amber);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
}

/* ROUTE CARD */
.route-red {
    background: #1c0a0a;
    border: 2px solid #ef4444;
    border-radius: 14px;
    padding: 18px;
}
.route-blue {
    background: #071520;
    border: 2px solid #38bdf8;
    border-radius: 14px;
    padding: 18px;
}

/* SCORE RING */
.score-ring {
    width: 140px; height: 140px;
    border-radius: 50%;
    background: conic-gradient(var(--green) 0% 72%, var(--border) 72% 100%);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto;
    position: relative;
}
.score-ring::before {
    content: '';
    position: absolute;
    inset: 12px;
    border-radius: 50%;
    background: var(--bg1);
}
.score-num {
    position: relative; z-index: 1;
    font-size: 30px; font-weight: 900;
    color: var(--green2);
    font-family: 'Share Tech Mono';
}

/* PROGRESS BAR */
.pbar-bg { background: var(--border); border-radius: 20px; height: 8px; margin: 8px 0; }
.pbar-fill { height: 8px; border-radius: 20px; transition: width 0.5s; }

/* LOGIN */
.login-wrap {
    max-width: 420px; margin: 50px auto;
    background: var(--bg1);
    border: 1px solid var(--border);
    border-radius: 24px; padding: 44px;
    text-align: center;
}

/* BADGE */
.badge {
    display: inline-block;
    background: #0d2318;
    color: var(--green2);
    border: 1px solid #166534;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 11px; letter-spacing: 2px;
}
.badge-red {
    background: #1c0a0a; color: var(--red); border-color: #7f1d1d;
}

.stTextInput > div > div > input {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Exo 2' !important;
}
.stSelectbox > div > div { background: var(--bg2) !important; border-radius: 10px !important; }

div[data-testid="stMetricValue"] {
    color: var(--green2) !important;
    font-family: 'Share Tech Mono' !important;
}

/* SEPARATOR */
.sep { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

/* DRIVING SPEED BAR */
.speed-bar {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)


# ================================================
# LOGIN
# ================================================
if not st.session_state.logged_in:
    st.markdown("<div class='mt-title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='mt-sub'>Smart Emission Intelligence System</div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#22c55e;font-family:Exo 2;font-weight:900;margin-bottom:4px;'>Sign In</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569;font-size:12px;letter-spacing:2px;'>PROTECTING THE PLANET, ONE TRIP AT A TIME</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Your name")
        password = st.text_input("Password", type="password", placeholder="Password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌿 Launch MellowTech", use_container_width=True):
            if not username.strip():
                st.error("Please enter a username.")
            elif not password:
                st.error("Please enter a password.")
            else:
                st.session_state.logged_in = True
                st.session_state.username  = username.strip()
                st.success(f"Welcome, {username}! Let's drive cleaner 🌍")
                time.sleep(0.6)
                st.rerun()

        st.markdown("<p style='color:#334155;font-size:11px;margin-top:16px;'>Demo: any username + any password</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ================================================
# SIDEBAR
# ================================================
st.sidebar.markdown(f"""
<div style='padding:12px 0;'>
  <div style='font-family:Exo 2;color:#22c55e;font-size:20px;font-weight:900;letter-spacing:3px;'>MELLOWTECH</div>
  <div style='color:#475569;font-size:11px;letter-spacing:2px;margin-top:2px;'>EMISSION INTELLIGENCE</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"<div class='badge'>● SYSTEM ONLINE</div><br><br>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:#64748b;font-size:13px;'>👤 {st.session_state.username}</p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:#22c55e;font-size:13px;'>🌿 {st.session_state.green_points} Green Points</p>", unsafe_allow_html=True)

menu = st.sidebar.radio("", [
    "🏠 Dashboard",
    "🗺️ Smart Routes",
    "🚨 Emission Alerts",
    "📊 Analytics",
    "🏆 Eco Score",
    "🎁 Rewards",
    "👤 Profile"
])

if st.sidebar.button("🔓 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("<hr style='border-color:#1e293b;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#1e293b;font-size:10px;text-align:center;'>MellowTech v2.0 · Climate Innovation</p>", unsafe_allow_html=True)


# ================================================
# HELPERS
# ================================================
hour_now = dt.now().hour
is_rush  = 7 <= hour_now <= 9 or 16 <= hour_now <= 18

locations_coords = {
    "Home":     (-25.7461, 28.1881),
    "Work":     (-25.7580, 28.1890),
    "School":   (-25.7400, 28.2100),
    "Mall":     (-25.7650, 28.3120),
    "Hospital": (-25.7320, 28.2280),
    "Airport":  (-25.9180, 28.3820),
    "Park":     (-25.7280, 28.2450),
    "Garage":   (-25.7500, 28.1750),
}

def congestion_for(seed, hr):
    np.random.seed(seed)
    v = np.random.randint(15, 70)
    return min(100, v + 30 if 7 <= hr <= 9 or 16 <= hr <= 18 else v)

def emission_level(cong):
    if cong > 65: return "HIGH",   "#ef4444", "🔴"
    if cong > 40: return "MEDIUM", "#f59e0b", "🟡"
    return "LOW", "#22c55e", "🟢"


# ================================================
# DASHBOARD
# ================================================
if menu == "🏠 Dashboard":

    st.markdown("<div class='mt-title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='mt-sub'>Smart Climate & Emission Intelligence</div>", unsafe_allow_html=True)

    time_str  = dt.now().strftime("%H:%M:%S")
    date_str  = dt.now().strftime("%d %b %Y")
    rush_str  = "🔴 RUSH HOUR" if is_rush else "🟢 CLEAR"
    city_cong = 72 if is_rush else 34

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, time_str,   "CURRENT TIME",     "kv-blue",  "card"),
        (c2, rush_str,   "TRAFFIC STATUS",   "kv-red" if is_rush else "kv-green", "card card-red" if is_rush else "card"),
        (c3, f"{st.session_state.eco_score}/100", "ECO SCORE", "kv-green", "card"),
        (c4, f"{st.session_state.green_points} pts", "GREEN POINTS", "kv-green", "card"),
    ]
    for col, val, label, cls, card_cls in cards:
        with col:
            st.markdown(f"""<div class='{card_cls}'>
                <div class='kv {cls}'>{val}</div>
                <div class='kl'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Live emission status
    if is_rush:
        st.markdown("""<div class='alert-red'>
            <b style='color:#ef4444;font-size:16px;'>⚠️ HIGH EMISSION ALERT</b><br>
            <span style='color:#fca5a5;'>Rush hour detected — Heavy traffic + high fuel burn zones active in your area.
            Consider delaying your trip or choosing a blue route.</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='alert-green'>
            <b style='color:#22c55e;font-size:16px;'>✅ LOW EMISSION CONDITIONS</b><br>
            <span style='color:#86efac;'>Traffic is clear. Smooth driving conditions — ideal time to travel efficiently.</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("📡 Real-Time City Emission Pulse")
        locs  = list(locations_coords.keys())
        congs = [congestion_for(i * 7, hour_now) for i in range(len(locs))]
        pulse = pd.DataFrame({"Zone": locs, "Emission Level %": congs})
        st.bar_chart(pulse.set_index("Zone"))

    with col_right:
        st.subheader("🌍 Today's Impact")
        savings_co2 = round(st.session_state.green_points * 0.12, 2)
        fuel_saved  = round(st.session_state.green_points * 0.05, 2)
        trips       = st.session_state.trips_today

        st.markdown(f"""<div class='card'>
            <div class='kv kv-green'>{savings_co2} kg</div>
            <div class='kl'>CO₂ Saved Today</div>
        </div><br>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='card card-amber'>
            <div class='kv kv-amber'>R{fuel_saved}</div>
            <div class='kl'>Fuel Cost Saved</div>
        </div><br>""", unsafe_allow_html=True)

        st.markdown(f"""<div class='card card-blue'>
            <div class='kv kv-blue'>{trips}</div>
            <div class='kl'>Trips Completed</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)
    st.subheader("🌱 Why It Matters")
    st.markdown("""
    > **Vehicle emissions** are a leading cause of urban air pollution, contributing to respiratory diseases,
    > climate change, and reduced quality of life. MellowTech helps you **reduce your carbon footprint**
    > while saving money — every clean trip earns Green Points redeemable for real rewards.
    """)


# ================================================
# SMART ROUTES
# ================================================
elif menu == "🗺️ Smart Routes":

    st.markdown(f"<h1 style='color:#22c55e;font-family:Exo 2;font-weight:900;'>🗺️ Smart Route Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Choose cleaner routes — reduce emissions and earn Green Points.</p>", unsafe_allow_html=True)

    locs = list(locations_coords.keys())

    c1, c2, c3 = st.columns(3)
    with c1: origin = st.selectbox("📍 Origin", locs)
    with c2: dest   = st.selectbox("🏁 Destination", [l for l in locs if l != origin])
    with c3: leave  = st.slider("🕐 Departure Hour", 0, 23, hour_now)

    waypoints = st.multiselect("➕ Add Waypoints", [l for l in locs if l not in [origin, dest]])

    st.markdown("<br>", unsafe_allow_html=True)

    # Simulate two routes
    np.random.seed(leave + ord(origin[0]) + ord(dest[0]))
    cong_a = min(100, np.random.randint(10, 45))
    cong_b = min(100, np.random.randint(50, 90) + (25 if is_rush else 0))

    dist_a = round(np.random.uniform(4, 18), 1)
    dist_b = round(dist_a * np.random.uniform(0.8, 1.3), 1)
    time_a = int(dist_a * 1.5 + cong_a * 0.3)
    time_b = int(dist_b * 1.5 + cong_b * 0.5)
    fuel_a = round(dist_a * 0.08, 2)
    fuel_b = round(dist_b * 0.08 + cong_b * 0.005, 2)
    co2_a  = round(fuel_a * 2.31, 2)
    co2_b  = round(fuel_b * 2.31, 2)

    colA, colB = st.columns(2)

    with colA:
        st.markdown(f"""<div class='route-blue'>
            <div style='font-size:18px;font-weight:800;color:#38bdf8;'>🔵 ROUTE A — CLEAN ROUTE</div>
            <div style='color:#7dd3fc;font-size:12px;letter-spacing:2px;margin-bottom:12px;'>RECOMMENDED · LOW EMISSIONS</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
                <div><div style='font-size:24px;font-weight:900;color:#38bdf8;font-family:Share Tech Mono;'>{cong_a}%</div><div style='color:#64748b;font-size:11px;'>CONGESTION</div></div>
                <div><div style='font-size:24px;font-weight:900;color:#38bdf8;font-family:Share Tech Mono;'>{time_a} min</div><div style='color:#64748b;font-size:11px;'>EST. TIME</div></div>
                <div><div style='font-size:24px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{dist_a} km</div><div style='color:#64748b;font-size:11px;'>DISTANCE</div></div>
                <div><div style='font-size:24px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{co2_a} kg</div><div style='color:#64748b;font-size:11px;'>CO₂ EMITTED</div></div>
            </div>
            <div style='margin-top:14px;background:#0a1a2e;border-radius:8px;padding:10px;font-size:13px;color:#7dd3fc;'>
                ✅ Smooth traffic flow · Lower fuel burn · +15 Green Points
            </div>
        </div>""", unsafe_allow_html=True)

    with colB:
        st.markdown(f"""<div class='route-red'>
            <div style='font-size:18px;font-weight:800;color:#ef4444;'>🔴 ROUTE B — HIGH EMISSION ROUTE</div>
            <div style='color:#fca5a5;font-size:12px;letter-spacing:2px;margin-bottom:12px;'>AVOID · HEAVY TRAFFIC</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
                <div><div style='font-size:24px;font-weight:900;color:#ef4444;font-family:Share Tech Mono;'>{cong_b}%</div><div style='color:#64748b;font-size:11px;'>CONGESTION</div></div>
                <div><div style='font-size:24px;font-weight:900;color:#ef4444;font-family:Share Tech Mono;'>{time_b} min</div><div style='color:#64748b;font-size:11px;'>EST. TIME</div></div>
                <div><div style='font-size:24px;font-weight:900;color:#f87171;font-family:Share Tech Mono;'>{dist_b} km</div><div style='color:#64748b;font-size:11px;'>DISTANCE</div></div>
                <div><div style='font-size:24px;font-weight:900;color:#f87171;font-family:Share Tech Mono;'>{co2_b} kg</div><div style='color:#64748b;font-size:11px;'>CO₂ EMITTED</div></div>
            </div>
            <div style='margin-top:14px;background:#1c0808;border-radius:8px;padding:10px;font-size:13px;color:#fca5a5;'>
                ⚠️ Stop-and-go traffic · High idling · Increased fuel burn
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div class='alert-green'>
        <b style='color:#22c55e;'>💡 Smart Advisor</b><br>
        <span style='color:#86efac;'>Choosing Route A over Route B saves <b>{round(co2_b - co2_a, 2)} kg CO₂</b> and approximately
        <b>R{round((fuel_b - fuel_a)*20, 2)}</b> in fuel costs. You will earn <b>+15 Green Points</b> for this trip.</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✅ Take Clean Route — Start Trip", use_container_width=True):
        st.session_state.green_points += 15
        st.session_state.trips_today  += 1
        st.session_state.eco_score     = min(100, st.session_state.eco_score + 1)
        st.success(f"🌿 Trip started! +15 Green Points added. Total: {st.session_state.green_points} pts")

    # Map
    st.subheader("🗺️ Route Map")
    route      = [origin] + waypoints + [dest]
    route_pts  = [locations_coords[r] for r in route]
    map_df     = pd.DataFrame(route_pts, columns=["lat", "lon"])
    st.map(map_df, zoom=12)

    for i, stop in enumerate(route):
        icon = "🟢" if i == 0 else ("🏁" if i == len(route) - 1 else "📍")
        st.markdown(f"{icon} **{stop}**")


# ================================================
# EMISSION ALERTS
# ================================================
elif menu == "🚨 Emission Alerts":

    st.markdown(f"<h1 style='color:#ef4444;font-family:Exo 2;font-weight:900;'>🚨 Real-Time Emission Alerts</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Live diagnostics & driving behaviour intelligence.</p>", unsafe_allow_html=True)

    # Simulate real-time data
    np.random.seed(hour_now * 3)
    emission_pct = np.random.randint(20, 95) if is_rush else np.random.randint(10, 55)
    speed_kmh    = np.random.randint(15, 45) if is_rush else np.random.randint(50, 100)
    idle_mins    = np.random.randint(0, 8)
    rpm          = np.random.randint(800, 4000)
    em_level, em_color, em_icon = emission_level(emission_pct)

    # Main alert
    if emission_pct > 65:
        st.markdown(f"""<div class='alert-red'>
            <div style='font-size:20px;font-weight:900;color:#ef4444;'>{em_icon} HIGH EMISSION DETECTED</div>
            <div style='color:#fca5a5;margin-top:6px;font-size:14px;'>
                Your vehicle is producing above-normal emissions right now.<br>
                <b>Action required:</b> Reduce speed · Avoid acceleration · Check engine diagnostics
            </div>
        </div>""", unsafe_allow_html=True)
    elif emission_pct > 40:
        st.markdown(f"""<div class='alert-amber'>
            <div style='font-size:20px;font-weight:900;color:#f59e0b;'>{em_icon} MODERATE EMISSIONS</div>
            <div style='color:#fde68a;margin-top:6px;font-size:14px;'>
                Emissions slightly elevated — likely due to traffic congestion.<br>
                <b>Tip:</b> Maintain steady speed and avoid sudden braking.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='alert-green'>
            <div style='font-size:20px;font-weight:900;color:#22c55e;'>{em_icon} LOW EMISSIONS — CLEAN DRIVING</div>
            <div style='color:#86efac;margin-top:6px;font-size:14px;'>
                Excellent! Your vehicle is running efficiently right now.<br>
                Keep up the steady speed and earn Green Points.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, f"{emission_pct}%", "EMISSION LEVEL", "kv-red" if emission_pct > 65 else ("kv-amber" if emission_pct > 40 else "kv-green"), "card-red" if emission_pct > 65 else "card"),
        (c2, f"{speed_kmh} km/h", "CURRENT SPEED", "kv-blue", "card-blue"),
        (c3, f"{idle_mins} min", "IDLE TIME", "kv-amber" if idle_mins > 2 else "kv-green", "card-amber" if idle_mins > 2 else "card"),
        (c4, f"{rpm} RPM", "ENGINE RPM", "kv-red" if rpm > 3000 else "kv-green", "card-red" if rpm > 3000 else "card"),
    ]
    for col, val, lbl, vcls, ccls in metrics:
        with col:
            st.markdown(f"""<div class='card {ccls}'>
                <div class='kv {vcls}'>{val}</div>
                <div class='kl'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Speed vs Emissions explainer
    st.subheader("⚡ Speed & Emission Relationship")
    speeds   = list(range(0, 130, 10))
    # Emission is high at very low speed (idling/congestion) and very high speed
    em_curve = [85, 80, 70, 55, 38, 25, 20, 18, 22, 30, 42, 58, 75]
    speed_df = pd.DataFrame({"Speed (km/h)": speeds, "Relative Emission %": em_curve})
    st.line_chart(speed_df.set_index("Speed (km/h)"))

    st.markdown("""<div class='alert-green'>
        <b style='color:#22c55e;'>🚗 Key Insight:</b>
        <span style='color:#86efac;'> Vehicles travelling at a <b>moderate, steady speed (60–80 km/h)</b> produce the LEAST pollution.
        Stop-and-go traffic (0–30 km/h) causes excessive idling and acceleration, dramatically increasing emissions.
        Speeding above 100 km/h also burns significantly more fuel.</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Action system
    st.subheader("🔧 Action Plan — What To Do Now")
    actions = [
        ("🔍 Check Engine / OBD Diagnostics", "Your vehicle may have an engine or exhaust fault causing high emissions. Run an OBD scan or visit a mechanic.", "#ef4444"),
        ("⛽ Reduce Fuel Waste Driving Mode",  "Avoid rapid acceleration · Maintain steady 60–80 km/h · Reduce engine RPM · Coast to slow down.", "#f59e0b"),
        ("🔧 Service Required",                "Consider: Oil change · Air filter replacement · Fuel injector cleaning · Exhaust system check.", "#38bdf8"),
        ("🚫 Stop Idling Warning",             "Switch off engine if idle for more than 1 minute. Idling wastes fuel and spikes emissions unnecessarily.", "#f59e0b"),
        ("🗺️ Switch to Cleaner Route",         "Less traffic = less smoke = more fuel efficiency. Use Smart Routes to find a blue-coded path.", "#22c55e"),
        ("⚠️ Emission Risk Warning",           "Your vehicle may exceed acceptable emission levels. This could affect compliance with future regulations.", "#ef4444"),
    ]
    for title, desc, color in actions:
        st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-left:3px solid {color};
                         border-radius:10px;padding:14px;margin-bottom:8px;'>
            <div style='color:{color};font-weight:700;font-size:15px;'>{title}</div>
            <div style='color:#94a3b8;font-size:13px;margin-top:4px;'>{desc}</div>
        </div>""", unsafe_allow_html=True)


# ================================================
# ANALYTICS
# ================================================
elif menu == "📊 Analytics":

    st.markdown(f"<h1 style='color:#38bdf8;font-family:Exo 2;font-weight:900;'>📊 Traffic & Emission Analytics</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Hourly Trends", "📍 Zone Emissions", "💰 Cost Impact", "🌡️ Weekly Heatmap"])

    with tab1:
        hours = list(range(24))
        np.random.seed(5)
        base_em = np.random.randint(15, 50, 24).tolist()
        emissions = [min(100, e + 35 if 7 <= h <= 9 or 16 <= h <= 18 else e) for e, h in zip(base_em, hours)]
        speeds    = [max(10, 85 - em // 2 + np.random.randint(-5, 5)) for em in emissions]
        fuel_burn = [round(em * 0.08 + np.random.uniform(0, 2), 1) for em in emissions]

        df_hourly = pd.DataFrame({
            "Hour":           hours,
            "Emission %":     emissions,
            "Avg Speed km/h": speeds,
            "Fuel L/100km":   fuel_burn,
        }).set_index("Hour")

        st.subheader("24-Hour Emission & Speed Trends")
        st.line_chart(df_hourly)

        peak_h = hours[np.argmax(emissions)]
        st.warning(f"⚠️ Peak emissions at **{peak_h}:00** ({max(emissions)}%) — corresponds to morning/evening rush hour.")
        st.success("✅ Cleanest travel window: **10:00–15:00** and **20:00–06:00**")

    with tab2:
        locs  = list(locations_coords.keys())
        np.random.seed(33)
        congs = [congestion_for(i * 11, hour_now) for i in range(len(locs))]
        em_lvls = [emission_level(c) for c in congs]

        zone_df = pd.DataFrame({
            "Zone": locs,
            "Congestion %": congs,
            "Emission Level": [e[0] for e in em_lvls],
        })
        st.subheader("Zone Emission Status")
        for _, row in zone_df.iterrows():
            lvl, col, icon = emission_level(row["Congestion %"])
            pct = row["Congestion %"]
            st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-radius:10px;padding:14px;margin-bottom:8px;'>
                <div style='display:flex;justify-content:space-between;'>
                    <span style='font-weight:700;font-size:15px;'>{icon} {row["Zone"]}</span>
                    <span class='badge' style='background:{col}22;color:{col};border-color:{col}55;'>{lvl}</span>
                </div>
                <div class='pbar-bg'><div class='pbar-fill' style='width:{pct}%;background:{col};'></div></div>
                <div style='color:#64748b;font-size:12px;'>{pct}% congestion</div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.subheader("💰 Fuel Cost Impact Estimator")
        weekly_km  = st.slider("Weekly driving distance (km)", 50, 500, 200)
        fuel_price = st.slider("Fuel price (R/litre)", 18, 26, 22)
        drive_style = st.selectbox("Driving style", ["Aggressive (stop-and-go)", "Moderate (steady speed)", "Eco (smooth & efficient)"])

        consumption = {"Aggressive (stop-and-go)": 12, "Moderate (steady speed)": 8, "Eco (smooth & efficient)": 6}
        litres_week = weekly_km / 100 * consumption[drive_style]
        cost_week   = round(litres_week * fuel_price, 2)
        cost_month  = round(cost_week * 4.3, 2)
        co2_week    = round(litres_week * 2.31, 2)

        eco_litres = weekly_km / 100 * 6
        eco_cost   = round(eco_litres * fuel_price, 2)
        saving     = round(cost_week - eco_cost, 2)

        ca, cb, cc, cd = st.columns(4)
        ca.metric("Weekly Fuel Cost", f"R{cost_week}")
        cb.metric("Monthly Fuel Cost", f"R{cost_month}")
        cc.metric("CO₂ per Week", f"{co2_week} kg")
        cd.metric("Potential Weekly Saving", f"R{max(0, saving)}", delta=f"-R{max(0, saving)}" if saving > 0 else "")

        if saving > 0:
            st.markdown(f"""<div class='alert-amber'>
                <b style='color:#f59e0b;'>💡 Cost Intelligence:</b>
                <span style='color:#fde68a;'>Switching to Eco driving style could save you <b>R{saving}/week</b>
                (R{round(saving*52, 0)}/year) and reduce your CO₂ output by <b>{round(co2_week - weekly_km/100*6*2.31, 1)} kg/week</b>.</span>
            </div>""", unsafe_allow_html=True)

    with tab4:
        days  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        hrs   = list(range(6, 21))
        np.random.seed(42)
        heat  = np.random.randint(10, 80, (7, len(hrs)))
        for i in range(7):
            for j, h in enumerate(hrs):
                if h in [7, 8, 17, 18] and i < 5:
                    heat[i][j] = min(100, heat[i][j] + 35)
        heat_df = pd.DataFrame(heat, index=days, columns=[f"{h}:00" for h in hrs])
        st.subheader("Weekly Emission Heatmap (% Congestion)")
        st.dataframe(heat_df.style.background_gradient(cmap="RdYlGn_r"), use_container_width=True)
        st.caption("Red = heavy congestion + high emissions · Green = smooth flow + low emissions")


# ================================================
# ECO SCORE
# ================================================
elif menu == "🏆 Eco Score":

    st.markdown(f"<h1 style='color:#22c55e;font-family:Exo 2;font-weight:900;'>🏆 Eco Score & Driver Rating</h1>", unsafe_allow_html=True)

    score = st.session_state.eco_score
    if score >= 80:   grade, grade_col, grade_label = "A", "#22c55e", "Excellent Eco Driver"
    elif score >= 65: grade, grade_col, grade_label = "B", "#4ade80", "Good Eco Driver"
    elif score >= 50: grade, grade_col, grade_label = "C", "#f59e0b", "Average Driver"
    else:             grade, grade_col, grade_label = "D", "#ef4444", "High Emission Driver"

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(f"""<div class='card' style='text-align:center;padding:30px;'>
            <div style='font-size:80px;font-weight:900;color:{grade_col};font-family:Share Tech Mono;
                        text-shadow:0 0 30px {grade_col}88;'>{grade}</div>
            <div style='font-size:42px;font-weight:900;color:{grade_col};font-family:Share Tech Mono;'>{score}/100</div>
            <div style='color:#64748b;font-size:12px;letter-spacing:2px;margin-top:8px;'>{grade_label.upper()}</div>
            <div style='color:#475569;font-size:12px;margin-top:12px;'>Air Risk Score: <b style='color:{grade_col};'>{100-score}/100</b></div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.subheader("📈 Weekly Performance")
        weeks  = ["6 wks ago","5 wks ago","4 wks ago","3 wks ago","2 wks ago","Last week","This week"]
        scores = st.session_state.weekly_scores
        week_df = pd.DataFrame({"Week": weeks, "Eco Score": scores})
        st.line_chart(week_df.set_index("Week"))

        trend = scores[-1] - scores[-2]
        if trend > 0:
            st.success(f"📈 Improving! +{trend} points vs last week. Keep it up!")
        elif trend < 0:
            st.warning(f"📉 Score dropped {abs(trend)} points. Try choosing cleaner routes.")
        else:
            st.info("➡️ Score stable this week.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Score Breakdown")

    factors = [
        ("Route Choices",          78, "#22c55e"),
        ("Speed Consistency",      65, "#4ade80"),
        ("Idle Time Management",   82, "#22c55e"),
        ("Trip Efficiency",        70, "#f59e0b"),
        ("Vehicle Emission Level", 55, "#f59e0b"),
        ("Carpooling Bonus",       40, "#ef4444"),
    ]
    for name, val, color in factors:
        st.markdown(f"""<div style='margin-bottom:12px;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
                <span style='font-size:14px;'>{name}</span>
                <span style='color:{color};font-weight:700;font-size:14px;'>{val}/100</span>
            </div>
            <div class='pbar-bg'><div class='pbar-fill' style='width:{val}%;background:{color};'></div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Leaderboard
    st.subheader("🏅 Driver Leaderboard")
    lb_data = {
        "Rank": ["🥇 1","🥈 2","🥉 3","4","5"],
        "Driver": ["EcoDriver_01","GreenWheels","CleanCommuter", st.session_state.username, "QuickRacer"],
        "Eco Score": [96, 91, 88, score, 43],
        "Green Points": [1240, 985, 872, st.session_state.green_points, 120],
        "CO₂ Saved (kg)": [148, 118, 104, round(st.session_state.green_points * 0.12, 1), 14],
    }
    lb_df = pd.DataFrame(lb_data)
    st.dataframe(lb_df, use_container_width=True, hide_index=True)


# ================================================
# REWARDS
# ================================================
elif menu == "🎁 Rewards":

    st.markdown(f"<h1 style='color:#f59e0b;font-family:Exo 2;font-weight:900;'>🎁 MellowTech Rewards Card</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Convert your Green Points into real-world rewards.</p>", unsafe_allow_html=True)

    pts = st.session_state.green_points

    st.markdown(f"""<div style='background:linear-gradient(135deg,#0f2a0a,#1a3a10);
                     border:1px solid #166534;border-radius:20px;padding:28px;margin-bottom:24px;
                     position:relative;overflow:hidden;'>
        <div style='position:absolute;right:20px;top:20px;font-size:48px;opacity:0.15;'>🌿</div>
        <div style='font-family:Share Tech Mono;font-size:13px;color:#86efac;letter-spacing:3px;'>MELLOWTECH REWARDS CARD</div>
        <div style='font-size:42px;font-weight:900;color:#4ade80;margin:8px 0;font-family:Share Tech Mono;'>{pts} pts</div>
        <div style='color:#22c55e;font-size:14px;'>Card Holder: {st.session_state.username}</div>
        <div style='color:#64748b;font-size:12px;margin-top:4px;'>{dt.now().strftime("%B %Y")} · ACTIVE</div>
    </div>""", unsafe_allow_html=True)

    rewards = [
        ("⛽ Fuel Voucher",            50,  "Save R10 at participating fuel stations",   "#f59e0b"),
        ("⛽ Petrol Discount (10%)",   120, "10% off your next full tank",                "#f59e0b"),
        ("🛒 Shopping Voucher R50",    100, "Redeem at partner retailers",                "#38bdf8"),
        ("🚌 Public Transport Credit", 80,  "Bus or taxi credit for 5 trips",             "#22c55e"),
        ("🔧 Free Vehicle Check",      200, "Emission diagnostic + engine check",         "#a78bfa"),
        ("🌱 Tree Planting Credit",    30,  "Sponsor a tree planted in your name",        "#22c55e"),
        ("🎟️ Partner Discounts",       60,  "Discounts at eco-friendly partner stores",   "#38bdf8"),
        ("🏅 Premium Eco Status",      500, "Unlock premium leaderboard + extra points",  "#f59e0b"),
    ]

    cols = st.columns(2)
    for i, (name, cost, desc, color) in enumerate(rewards):
        with cols[i % 2]:
            can_afford = pts >= cost
            btn_style  = f"background:{color}22;border:1px solid {color}55;color:{color};" if can_afford else "background:#0a0f1e;border:1px solid #1e293b;color:#334155;"
            st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-radius:14px;padding:16px;margin-bottom:12px;'>
                <div style='font-size:16px;font-weight:700;color:{"white" if can_afford else "#334155"};'>{name}</div>
                <div style='color:#64748b;font-size:13px;margin:4px 0;'>{desc}</div>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-top:10px;'>
                    <span style='color:{color};font-weight:900;font-family:Share Tech Mono;font-size:18px;'>{cost} pts</span>
                    <span style='padding:6px 14px;border-radius:20px;font-size:12px;font-weight:700;{btn_style}'>
                        {"✅ REDEEM" if can_afford else "🔒 LOCKED"}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🌿 How to Earn More Green Points")
    earn_tips = [
        ("🗺️ Choose Blue Routes",       "+15 pts per clean trip"),
        ("🚗 Maintain Steady Speed",    "+5 pts per trip under 70% emission"),
        ("🚌 Use Public Transport",     "+20 pts per public transport trip"),
        ("🚫 No Idling",                "+3 pts when idle time < 1 min"),
        ("🤝 Carpool / Rideshare",      "+25 pts per shared trip"),
        ("🔧 Service Your Vehicle",     "+50 pts after emission check-up"),
    ]
    cols2 = st.columns(3)
    for i, (tip, pts_earn) in enumerate(earn_tips):
        with cols2[i % 3]:
            st.markdown(f"""<div style='background:#071a0e;border:1px solid #14532d;border-radius:10px;padding:14px;margin-bottom:10px;text-align:center;'>
                <div style='font-size:15px;font-weight:700;color:#4ade80;'>{tip}</div>
                <div style='color:#22c55e;font-size:18px;font-weight:900;font-family:Share Tech Mono;margin-top:6px;'>{pts_earn}</div>
            </div>""", unsafe_allow_html=True)


# ================================================
# PROFILE
# ================================================
elif menu == "👤 Profile":

    st.markdown(f"<h1 style='color:#38bdf8;font-family:Exo 2;font-weight:900;'>👤 Driver Profile</h1>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])

    with c1:
        score  = st.session_state.eco_score
        grade  = "A" if score >= 80 else ("B" if score >= 65 else ("C" if score >= 50 else "D"))
        g_col  = "#22c55e" if score >= 80 else ("#4ade80" if score >= 65 else ("#f59e0b" if score >= 50 else "#ef4444"))
        st.markdown(f"""<div class='card' style='text-align:center;padding:28px;'>
            <div style='font-size:56px;'>🌿</div>
            <div style='font-size:22px;font-weight:900;color:#22c55e;margin-top:8px;font-family:Exo 2;'>{st.session_state.username}</div>
            <div class='badge' style='margin-top:6px;'>ECO DRIVER · GRADE {grade}</div>
            <hr style='border-color:#1e293b;margin:16px 0;'>
            <div style='color:#64748b;font-size:12px;'>Member since {dt.now().strftime("%b %Y")}</div>
            <div style='margin-top:12px;'>
                <div style='font-size:28px;font-weight:900;color:{g_col};font-family:Share Tech Mono;'>{score}/100</div>
                <div style='color:#64748b;font-size:11px;letter-spacing:2px;'>ECO SCORE</div>
            </div>
            <div style='margin-top:12px;'>
                <div style='font-size:28px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{st.session_state.green_points}</div>
                <div style='color:#64748b;font-size:11px;letter-spacing:2px;'>GREEN POINTS</div>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.subheader("⚙️ Preferences")
        new_name   = st.text_input("Display Name", value=st.session_state.username)
        home_loc   = st.selectbox("🏠 Home Location", list(locations_coords.keys()),
                                  index=list(locations_coords.keys()).index(st.session_state.home_location))
        drive_pref = st.selectbox("🚗 Default Driving Mode", ["Eco Mode", "Normal Mode", "Fast Mode"])
        notifs     = st.toggle("🔔 Enable Emission Alerts", value=True)
        pub_trans  = st.toggle("🚌 Promote Public Transport Routes", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Preferences", use_container_width=True):
            st.session_state.username       = new_name
            st.session_state.home_location  = home_loc
            st.session_state.driving_mode   = drive_pref
            st.success("✅ Preferences saved!")
            time.sleep(0.4)
            st.rerun()

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)

    st.subheader("📊 My Environmental Impact Summary")
    co2_total  = round(st.session_state.green_points * 0.12, 2)
    fuel_total = round(st.session_state.green_points * 0.05, 2)
    money_saved = round(fuel_total * 22, 2)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Total CO₂ Saved",     f"{co2_total} kg",  help="CO₂ not emitted due to clean route choices")
    mc2.metric("Fuel Saved",          f"{fuel_total} L",  help="Litres of fuel saved")
    mc3.metric("Money Saved",         f"R{money_saved}",  help="Estimated Rand savings on fuel")
    mc4.metric("Trips Completed",     st.session_state.trips_today)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div class='alert-green'>
        <b style='color:#22c55e;'>🌍 Your Climate Contribution</b><br>
        <span style='color:#86efac;'>By using MellowTech, you have helped reduce urban air pollution and contributed to
        South Africa's climate change mitigation goals. Every clean trip counts towards a healthier planet for future generations.</span>
    </div>""", unsafe_allow_html=True)
