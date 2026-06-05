import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="MellowTech | Smart Emission Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
defaults = {
    "logged_in": False,
    "username": "",
    "home_location": "Home",
    "green_points": 0,
    "eco_score": 72,
    "loaded": False,
    "trips_today": 0,
    "weekly_scores": [55, 61, 58, 67, 70, 68, 72],
    "page": "Dashboard",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.loaded:
    with st.spinner("Starting MellowTech..."):
        time.sleep(1)
    st.session_state.loaded = True

# ------------------------------------------------
# STYLE — icon-only sidebar + driver-friendly UI
# ------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
    --green:  #22c55e;
    --green2: #4ade80;
    --red:    #ef4444;
    --amber:  #f59e0b;
    --blue:   #38bdf8;
    --bg0:    #030712;
    --bg1:    #0a0f1e;
    --bg2:    #0f1929;
    --border: #1e293b;
    --text:   #e2e8f0;
    --muted:  #475569;
}

* { font-family: 'Exo 2', sans-serif; }
.stApp { background: var(--bg0); color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }

/* ===================== */
/* ICON-ONLY SIDEBAR     */
/* ===================== */
[data-testid="stSidebar"] {
    background: #060b18 !important;
    border-right: 1px solid #0f172a !important;
    min-width: 72px !important;
    max-width: 72px !important;
    width: 72px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    width: 72px !important;
}

/* Hide ALL text in sidebar — show only icons */
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not(.sidebar-icon),
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
    display: none !important;
}

/* Hide radio circles */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 0 !important;
    border: none !important;
    background: transparent !important;
    width: 72px !important;
    height: 64px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 28px !important;
    cursor: pointer;
    transition: background 0.2s;
    position: relative;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #0f172a !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
    background: #0d2318 !important;
    border-left: 3px solid var(--green) !important;
}

/* Hide the radio dot */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* The emoji text node — keep only the emoji character */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:last-child {
    font-size: 26px !important;
    line-height: 1 !important;
}

/* Hide everything after the first emoji character in label text */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:last-child > p {
    display: block !important;
    font-size: 0 !important;  /* hide text, show emoji via first-letter trick below */
}

/* Sidebar logout button */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: none !important;
    font-size: 22px !important;
    width: 72px !important;
    padding: 16px 0 !important;
    color: #475569 !important;
    cursor: pointer;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: #0f172a !important;
    color: #ef4444 !important;
}

/* ===================== */
/* DRIVER-FRIENDLY CARDS */
/* ===================== */
.big-card {
    background: linear-gradient(135deg, var(--bg1), var(--bg2));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.15s, border-color 0.15s;
}
.big-card:hover { transform: translateY(-2px); }
.big-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, var(--green), transparent);
}
.big-card-red::before   { background: linear-gradient(90deg, transparent, var(--red), transparent); }
.big-card-amber::before { background: linear-gradient(90deg, transparent, var(--amber), transparent); }
.big-card-blue::before  { background: linear-gradient(90deg, transparent, var(--blue), transparent); }

.big-num { font-size: 40px; font-weight: 900; font-family: 'Share Tech Mono'; }
.big-label { font-size: 13px; letter-spacing: 2px; color: var(--muted); text-transform: uppercase; margin-top: 6px; }

/* STATUS BANNER */
.banner-red {
    background: #1c0a0a; border: 1px solid #7f1d1d;
    border-left: 5px solid var(--red);
    border-radius: 14px; padding: 20px 24px; margin: 12px 0;
    font-size: 16px;
    animation: pulse-red 2s infinite;
}
@keyframes pulse-red {
    0%,100% { box-shadow: 0 0 0 0 #ef444400; }
    50%      { box-shadow: 0 0 16px 4px #ef444422; }
}
.banner-green {
    background: #071a0e; border: 1px solid #14532d;
    border-left: 5px solid var(--green);
    border-radius: 14px; padding: 20px 24px; margin: 12px 0;
    font-size: 16px;
}
.banner-amber {
    background: #1a1203; border: 1px solid #78350f;
    border-left: 5px solid var(--amber);
    border-radius: 14px; padding: 20px 24px; margin: 12px 0;
    font-size: 16px;
}

/* BIG ACTION BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #166534, #15803d) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 16px !important;
    transition: all 0.2s !important;
    font-family: 'Exo 2' !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #15803d, #16a34a) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px #22c55e33 !important;
}

/* ROUTE CARDS */
.route-blue {
    background: #071520; border: 2px solid #38bdf8;
    border-radius: 16px; padding: 22px;
}
.route-red {
    background: #1c0a0a; border: 2px solid #ef4444;
    border-radius: 16px; padding: 22px;
}

/* PROGRESS BAR */
.pbar-bg { background: var(--border); border-radius: 20px; height: 10px; margin: 8px 0; }
.pbar-fill { height: 10px; border-radius: 20px; }

/* TITLE */
.mt-title {
    font-size: 46px; font-weight: 900; color: var(--green2);
    text-shadow: 0 0 30px #22c55e88;
    letter-spacing: 3px; text-align: center; line-height: 1;
}
.mt-sub {
    text-align: center; color: var(--muted);
    font-size: 12px; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 28px;
}

/* INPUTS */
.stTextInput > div > div > input {
    background: var(--bg2) !important; border: 1px solid var(--border) !important;
    border-radius: 12px !important; color: white !important;
    font-size: 16px !important; padding: 12px !important;
}
.stSelectbox > div > div { background: var(--bg2) !important; border-radius: 12px !important; }
div[data-testid="stMetricValue"] { color: var(--green2) !important; font-family: 'Share Tech Mono' !important; }

/* BADGE */
.badge {
    display: inline-block; background: #0d2318;
    color: var(--green2); border: 1px solid #166534;
    border-radius: 20px; padding: 4px 14px; font-size: 11px; letter-spacing: 2px;
}

.sep { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
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
        st.markdown("""<div style='background:#0a0f1e;border:1px solid #1e293b;border-radius:24px;padding:40px;text-align:center;'>""", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#22c55e;font-weight:900;margin-bottom:4px;'>Sign In</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569;font-size:12px;letter-spacing:2px;'>PROTECTING THE PLANET, ONE TRIP AT A TIME</p><br>", unsafe_allow_html=True)

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
                time.sleep(0.5)
                st.rerun()

        st.markdown("<p style='color:#334155;font-size:11px;margin-top:16px;'>Demo: any username + any password</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ================================================
# SIDEBAR — icon only
# ================================================
# Logo area
st.sidebar.markdown("""
<div style='width:72px;height:64px;display:flex;align-items:center;justify-content:center;
            border-bottom:1px solid #0f172a;margin-bottom:4px;'>
  <span style='font-size:28px;'>🌿</span>
</div>
""", unsafe_allow_html=True)

# Navigation — only emojis shown (CSS hides all text after the emoji)
menu = st.sidebar.radio("", [
    "🏠",   # Dashboard
    "🗺️",   # Smart Routes
    "🚨",   # Emission Alerts
    "📊",   # Analytics
    "🏆",   # Eco Score
    "🎁",   # Rewards
    "👤",   # Profile
])

# Map emoji → page name for readability
page_map = {
    "🏠": "Dashboard",
    "🗺️": "Smart Routes",
    "🚨": "Emission Alerts",
    "📊": "Analytics",
    "🏆": "Eco Score",
    "🎁": "Rewards",
    "👤": "Profile",
}
page = page_map.get(menu, "Dashboard")

# Logout icon at bottom
st.sidebar.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
if st.sidebar.button("🔓"):
    st.session_state.logged_in = False
    st.rerun()
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Show current page name as tooltip/header
st.sidebar.markdown(f"""
<div style='position:fixed;left:72px;top:50%;transform:translateY(-50%);
            background:#0a0f1e;border:1px solid #1e293b;border-radius:8px;
            padding:6px 10px;font-size:11px;color:#22c55e;letter-spacing:1px;
            pointer-events:none;display:none;'>
  {page}
</div>
""", unsafe_allow_html=True)

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

def page_header(icon, title, color="#22c55e", subtitle=""):
    st.markdown(f"""
    <div style='margin-bottom:24px;'>
      <div style='font-size:36px;font-weight:900;color:{color};letter-spacing:2px;'>
        {icon} {title}
      </div>
      {"<div style='color:#475569;font-size:14px;margin-top:2px;'>"+subtitle+"</div>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)

# ================================================
# DASHBOARD
# ================================================
if page == "Dashboard":

    st.markdown("<div class='mt-title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='mt-sub'>Smart Climate & Emission Intelligence</div>", unsafe_allow_html=True)

    time_str = dt.now().strftime("%H:%M")
    rush_str = "🔴 RUSH HOUR" if is_rush else "🟢 ALL CLEAR"

    # 4 big driver-friendly KPI cards
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, time_str,   "TIME NOW",      "#38bdf8", "big-card big-card-blue"),
        (c2, rush_str,   "TRAFFIC",       "#ef4444" if is_rush else "#22c55e", "big-card big-card-red" if is_rush else "big-card"),
        (c3, f"{st.session_state.eco_score}/100", "ECO SCORE", "#22c55e", "big-card"),
        (c4, f"{st.session_state.green_points} pts", "GREEN PTS", "#4ade80", "big-card"),
    ]
    for col, val, lbl, color, cls in kpis:
        with col:
            st.markdown(f"""<div class='{cls}'>
                <div class='big-num' style='color:{color};'>{val}</div>
                <div class='big-label'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main status banner — BIG and clear for drivers
    if is_rush:
        st.markdown("""<div class='banner-red'>
            <div style='font-size:22px;font-weight:900;color:#ef4444;'>⚠️ RUSH HOUR — HIGH EMISSIONS</div>
            <div style='color:#fca5a5;margin-top:6px;font-size:16px;'>
                Heavy traffic detected. <b>Delay your trip</b> or use Smart Routes to find a cleaner path.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='banner-green'>
            <div style='font-size:22px;font-weight:900;color:#22c55e;'>✅ GOOD CONDITIONS — LOW EMISSIONS</div>
            <div style='color:#86efac;margin-top:6px;font-size:16px;'>
                Traffic is clear. Great time to travel. Drive at steady speed to earn Green Points.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("📡 City Emission Levels Right Now")
        locs  = list(locations_coords.keys())
        congs = [congestion_for(i * 7, hour_now) for i in range(len(locs))]
        st.bar_chart(pd.DataFrame({"Zone": locs, "Emission %": congs}).set_index("Zone"))

    with col_right:
        st.subheader("🌍 Your Impact Today")
        co2_s  = round(st.session_state.green_points * 0.12, 2)
        fuel_s = round(st.session_state.green_points * 0.05, 2)
        st.markdown(f"""
        <div class='big-card' style='margin-bottom:12px;'>
            <div class='big-num' style='color:#22c55e;'>{co2_s} kg</div>
            <div class='big-label'>CO₂ SAVED</div>
        </div>
        <div class='big-card big-card-amber' style='margin-bottom:12px;'>
            <div class='big-num' style='color:#f59e0b;'>R{round(fuel_s*22,2)}</div>
            <div class='big-label'>FUEL MONEY SAVED</div>
        </div>
        <div class='big-card big-card-blue'>
            <div class='big-num' style='color:#38bdf8;'>{st.session_state.trips_today}</div>
            <div class='big-label'>CLEAN TRIPS TODAY</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)
    st.markdown("""<div class='banner-green'>
        <b style='color:#22c55e;'>🌱 Why MellowTech Matters</b><br>
        <span style='color:#86efac;font-size:15px;'>Vehicle emissions cause air pollution, asthma, and climate change.
        MellowTech helps you drive cleaner, save fuel money, and earn rewards — all at once.</span>
    </div>""", unsafe_allow_html=True)


# ================================================
# SMART ROUTES
# ================================================
elif page == "Smart Routes":

    page_header("🗺️", "Smart Routes", "#22c55e", "Pick the clean route — save fuel, earn points")

    locs = list(locations_coords.keys())
    c1, c2 = st.columns(2)
    with c1:
        origin = st.selectbox("📍 Where are you?", locs, key="origin")
    with c2:
        dest   = st.selectbox("🏁 Where to?", [l for l in locs if l != origin], key="dest")

    leave = st.slider("🕐 What time are you leaving?", 0, 23, hour_now,
                      help="Drag to change your departure time")

    st.markdown("<br>", unsafe_allow_html=True)

    np.random.seed(leave + ord(origin[0]) + ord(dest[0]))
    cong_a = min(100, int(np.random.randint(10, 45)))
    cong_b = min(100, int(np.random.randint(55, 90) + (20 if is_rush else 0)))

    dist_a = round(float(np.random.uniform(4, 18)), 1)
    dist_b = round(float(dist_a * np.random.uniform(0.85, 1.25)), 1)
    time_a = int(dist_a * 1.5 + cong_a * 0.3)
    time_b = int(dist_b * 1.5 + cong_b * 0.5)
    co2_a  = round(dist_a * 0.08 * 2.31, 2)
    co2_b  = round((dist_b * 0.08 + cong_b * 0.005) * 2.31, 2)
    fuel_save = round((co2_b - co2_a) / 2.31 * 22, 2)

    colA, colB = st.columns(2)
    with colA:
        st.markdown(f"""<div class='route-blue'>
            <div style='font-size:20px;font-weight:900;color:#38bdf8;margin-bottom:14px;'>🔵 CLEAN ROUTE — TAKE THIS ONE</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:14px;'>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#38bdf8;font-family:Share Tech Mono;'>{cong_a}%</div>
                    <div style='color:#64748b;font-size:12px;'>CONGESTION</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#38bdf8;font-family:Share Tech Mono;'>{time_a} min</div>
                    <div style='color:#64748b;font-size:12px;'>TRAVEL TIME</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{dist_a} km</div>
                    <div style='color:#64748b;font-size:12px;'>DISTANCE</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{co2_a} kg</div>
                    <div style='color:#64748b;font-size:12px;'>CO₂</div>
                </div>
            </div>
            <div style='background:#0a1a2e;border-radius:10px;padding:12px;margin-top:14px;color:#7dd3fc;font-size:14px;'>
                ✅ Smooth flow · Less fuel · <b>+15 Green Points</b>
            </div>
        </div>""", unsafe_allow_html=True)

    with colB:
        st.markdown(f"""<div class='route-red'>
            <div style='font-size:20px;font-weight:900;color:#ef4444;margin-bottom:14px;'>🔴 HEAVY ROUTE — AVOID</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:14px;'>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#ef4444;font-family:Share Tech Mono;'>{cong_b}%</div>
                    <div style='color:#64748b;font-size:12px;'>CONGESTION</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#ef4444;font-family:Share Tech Mono;'>{time_b} min</div>
                    <div style='color:#64748b;font-size:12px;'>TRAVEL TIME</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#f87171;font-family:Share Tech Mono;'>{dist_b} km</div>
                    <div style='color:#64748b;font-size:12px;'>DISTANCE</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:32px;font-weight:900;color:#f87171;font-family:Share Tech Mono;'>{co2_b} kg</div>
                    <div style='color:#64748b;font-size:12px;'>CO₂</div>
                </div>
            </div>
            <div style='background:#1c0808;border-radius:10px;padding:12px;margin-top:14px;color:#fca5a5;font-size:14px;'>
                ⚠️ Stop-and-go · High idling · Wastes fuel
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div class='banner-green'>
        <b style='color:#22c55e;font-size:18px;'>💡 Choosing the clean route saves you R{max(0, fuel_save)} in fuel and {round(co2_b-co2_a,2)} kg CO₂</b>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅  START CLEAN TRIP  — Earn +15 Green Points", use_container_width=True):
        st.session_state.green_points += 15
        st.session_state.trips_today  += 1
        st.session_state.eco_score     = min(100, st.session_state.eco_score + 1)
        st.success(f"🌿 Clean trip started! You now have {st.session_state.green_points} Green Points.")

    st.subheader("🗺️ Map")
    map_df = pd.DataFrame([locations_coords[origin], locations_coords[dest]], columns=["lat","lon"])
    st.map(map_df, zoom=12)


# ================================================
# EMISSION ALERTS
# ================================================
elif page == "Emission Alerts":

    page_header("🚨", "Emission Alerts", "#ef4444", "Live vehicle & road diagnostics")

    np.random.seed(hour_now * 3)
    emission_pct = int(np.random.randint(20, 95) if is_rush else np.random.randint(10, 55))
    speed_kmh    = int(np.random.randint(15, 45) if is_rush else np.random.randint(50, 100))
    idle_mins    = int(np.random.randint(0, 8))
    rpm          = int(np.random.randint(800, 4000))
    em_level, em_color, em_icon = emission_level(emission_pct)

    # BIG clear banner
    if emission_pct > 65:
        st.markdown(f"""<div class='banner-red'>
            <div style='font-size:26px;font-weight:900;color:#ef4444;'>🔴 HIGH EMISSION DETECTED</div>
            <div style='color:#fca5a5;margin-top:8px;font-size:16px;'>
                Your vehicle is polluting heavily right now.<br>
                👉 <b>Slow down · Avoid acceleration · Check engine</b>
            </div>
        </div>""", unsafe_allow_html=True)
    elif emission_pct > 40:
        st.markdown(f"""<div class='banner-amber'>
            <div style='font-size:26px;font-weight:900;color:#f59e0b;'>🟡 MODERATE EMISSIONS</div>
            <div style='color:#fde68a;margin-top:8px;font-size:16px;'>
                Emissions a bit high — probably traffic congestion.<br>
                👉 <b>Keep a steady speed · Avoid braking hard</b>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='banner-green'>
            <div style='font-size:26px;font-weight:900;color:#22c55e;'>🟢 LOW EMISSIONS — GREAT DRIVING!</div>
            <div style='color:#86efac;margin-top:8px;font-size:16px;'>
                Your vehicle is running clean. Keep up the steady speed!
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    live = [
        (c1, f"{emission_pct}%", "EMISSION",  em_color),
        (c2, f"{speed_kmh}",     "SPEED km/h","#38bdf8"),
        (c3, f"{idle_mins} min", "IDLING",    "#f59e0b" if idle_mins > 2 else "#22c55e"),
        (c4, f"{rpm}",           "ENGINE RPM","#ef4444" if rpm > 3000 else "#22c55e"),
    ]
    for col, val, lbl, color in live:
        with col:
            st.markdown(f"""<div class='big-card'>
                <div class='big-num' style='color:{color};'>{val}</div>
                <div class='big-label'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("⚡ Speed Sweet Spot — Drive at 60–80 km/h")
    speeds   = list(range(0, 130, 10))
    em_curve = [85, 80, 70, 55, 38, 25, 20, 18, 22, 30, 42, 58, 75]
    st.line_chart(pd.DataFrame({"Speed (km/h)": speeds, "Emission Level %": em_curve}).set_index("Speed (km/h)"))
    st.markdown("""<div class='banner-green'>
        🚗 <b style='color:#22c55e;'>Best speed to drive: 60–80 km/h</b>
        <span style='color:#86efac;'> — uses least fuel, produces least pollution. Stop-and-go traffic is the worst.</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔧 What Should You Do Right Now?")

    actions = [
        ("🔍 Check Your Engine",         "Unusual emissions may mean an engine fault. Visit a mechanic or run an OBD scan.",        "#ef4444"),
        ("⛽ Drive at Steady Speed",      "Avoid sudden acceleration. Stay at 60–80 km/h. Reduces fuel burn significantly.",         "#f59e0b"),
        ("🔧 Service Your Vehicle",       "Oil change · Air filter · Fuel injectors · Exhaust check — all reduce emissions.",        "#38bdf8"),
        ("🚫 Turn Off When Idling",       "If stopped for more than 1 minute, switch off your engine. Saves fuel instantly.",        "#f59e0b"),
        ("🗺️ Take a Cleaner Route",       "Go to Smart Routes to find a less congested path with lower emissions.",                  "#22c55e"),
    ]
    for title, desc, color in actions:
        st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-left:4px solid {color};
                        border-radius:12px;padding:16px 20px;margin-bottom:10px;'>
            <div style='color:{color};font-weight:700;font-size:16px;'>{title}</div>
            <div style='color:#94a3b8;font-size:14px;margin-top:4px;'>{desc}</div>
        </div>""", unsafe_allow_html=True)


# ================================================
# ANALYTICS
# ================================================
elif page == "Analytics":

    page_header("📊", "Analytics", "#38bdf8", "Traffic & emission data for smarter decisions")

    tab1, tab2, tab3 = st.tabs(["📈 24h Trends", "📍 Zone Status", "💰 Fuel Cost Calculator"])

    with tab1:
        hours   = list(range(24))
        np.random.seed(5)
        base_em = np.random.randint(15, 50, 24).tolist()
        ems     = [min(100, e + 35 if 7 <= h <= 9 or 16 <= h <= 18 else e) for e, h in zip(base_em, hours)]
        spds    = [max(10, 85 - em // 2) for em in ems]
        st.subheader("Emission & Speed Over 24 Hours")
        st.line_chart(pd.DataFrame({"Hour": hours, "Emission %": ems, "Speed km/h": spds}).set_index("Hour"))
        peak_h = hours[int(np.argmax(ems))]
        st.warning(f"⚠️ Worst time to drive: **{peak_h}:00** — {max(ems)}% emission level")
        st.success("✅ Best time to drive: **10:00–15:00** — lowest congestion and emissions")

    with tab2:
        locs  = list(locations_coords.keys())
        congs = [congestion_for(i * 11, hour_now) for i in range(len(locs))]
        st.subheader("Area Emission Levels Now")
        for loc, cong in zip(locs, congs):
            lvl, color, icon = emission_level(cong)
            st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-radius:12px;
                            padding:14px 18px;margin-bottom:8px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-size:16px;font-weight:700;'>{icon} {loc}</span>
                    <span style='color:{color};font-weight:900;font-size:18px;font-family:Share Tech Mono;'>{cong}% — {lvl}</span>
                </div>
                <div class='pbar-bg' style='margin-top:8px;'>
                    <div class='pbar-fill' style='width:{cong}%;background:{color};'></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.subheader("💰 How Much Is Your Driving Costing You?")
        weekly_km   = st.slider("km driven per week", 50, 500, 200)
        fuel_price  = st.slider("Fuel price (R per litre)", 18, 26, 22)
        style       = st.selectbox("Your driving style", ["Stop-and-go (heavy traffic)", "Steady speed (normal)", "Smooth & efficient (eco)"])
        cons_map    = {"Stop-and-go (heavy traffic)": 12, "Steady speed (normal)": 8, "Smooth & efficient (eco)": 6}
        litres      = weekly_km / 100 * cons_map[style]
        cost_w      = round(litres * fuel_price, 2)
        eco_cost    = round(weekly_km / 100 * 6 * fuel_price, 2)
        saving      = round(max(0, cost_w - eco_cost), 2)
        co2_w       = round(litres * 2.31, 2)

        ca, cb, cc, cd = st.columns(4)
        ca.metric("Weekly Cost",  f"R{cost_w}")
        cb.metric("Monthly Cost", f"R{round(cost_w*4.3,2)}")
        cc.metric("CO₂/week",     f"{co2_w} kg")
        cd.metric("You could save", f"R{saving}/week")

        if saving > 0:
            st.markdown(f"""<div class='banner-amber'>
                <b style='color:#f59e0b;font-size:18px;'>💡 Driving smoother could save you R{saving}/week = R{round(saving*52)} per year!</b>
            </div>""", unsafe_allow_html=True)


# ================================================
# ECO SCORE
# ================================================
elif page == "Eco Score":

    page_header("🏆", "Eco Score", "#22c55e", "Your personal driving & emission rating")

    score = st.session_state.eco_score
    grade = "A" if score >= 80 else ("B" if score >= 65 else ("C" if score >= 50 else "D"))
    g_col = "#22c55e" if score >= 80 else ("#4ade80" if score >= 65 else ("#f59e0b" if score >= 50 else "#ef4444"))
    g_lbl = "Excellent Eco Driver" if score >= 80 else ("Good Driver" if score >= 65 else ("Average Driver" if score >= 50 else "High Polluter"))

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""<div class='big-card' style='padding:32px;text-align:center;'>
            <div style='font-size:90px;font-weight:900;color:{g_col};font-family:Share Tech Mono;
                        text-shadow:0 0 40px {g_col}88;line-height:1;'>{grade}</div>
            <div style='font-size:44px;font-weight:900;color:{g_col};font-family:Share Tech Mono;margin-top:4px;'>{score}/100</div>
            <div style='color:#64748b;font-size:13px;letter-spacing:2px;margin-top:8px;'>{g_lbl.upper()}</div>
            <div style='color:#475569;font-size:13px;margin-top:14px;'>Air Risk: <b style='color:{g_col};'>{100-score}/100</b></div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.subheader("📈 Your Progress This Month")
        weeks  = ["Wk 1","Wk 2","Wk 3","Wk 4","Wk 5","Wk 6","This Wk"]
        scores = st.session_state.weekly_scores
        st.line_chart(pd.DataFrame({"Week": weeks, "Eco Score": scores}).set_index("Week"))
        trend = scores[-1] - scores[-2]
        if trend > 0:   st.success(f"📈 Up {trend} points this week — keep driving clean!")
        elif trend < 0: st.warning(f"📉 Down {abs(trend)} points. Try using Smart Routes more.")
        else:           st.info("➡️ Score holding steady.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Score Breakdown")
    factors = [
        ("Route Choices",       78, "#22c55e"),
        ("Steady Speed",        65, "#4ade80"),
        ("Idle Time",           82, "#22c55e"),
        ("Trip Efficiency",     70, "#f59e0b"),
        ("Vehicle Emissions",   55, "#f59e0b"),
        ("Carpooling",          40, "#ef4444"),
    ]
    for name, val, color in factors:
        st.markdown(f"""<div style='margin-bottom:14px;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                <span style='font-size:15px;font-weight:600;'>{name}</span>
                <span style='color:{color};font-weight:900;font-size:16px;'>{val}/100</span>
            </div>
            <div class='pbar-bg'><div class='pbar-fill' style='width:{val}%;background:{color};'></div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🏅 Driver Leaderboard")
    lb = pd.DataFrame({
        "Rank":    ["🥇 1","🥈 2","🥉 3","4 YOU","5"],
        "Driver":  ["EcoDriver_01","GreenWheels","CleanCommuter", st.session_state.username, "QuickRacer"],
        "Score":   [96, 91, 88, score, 43],
        "Pts":     [1240, 985, 872, st.session_state.green_points, 120],
        "CO₂ Saved": [148, 118, 104, round(st.session_state.green_points * 0.12, 1), 14],
    })
    st.dataframe(lb, use_container_width=True, hide_index=True)


# ================================================
# REWARDS
# ================================================
elif page == "Rewards":

    page_header("🎁", "Rewards", "#f59e0b", "Turn your Green Points into real rewards")

    pts = st.session_state.green_points

    st.markdown(f"""<div style='background:linear-gradient(135deg,#0f2a0a,#1a3a10);
                    border:1px solid #166534;border-radius:20px;padding:28px;margin-bottom:24px;
                    position:relative;overflow:hidden;'>
        <div style='position:absolute;right:20px;top:16px;font-size:60px;opacity:0.1;'>🌿</div>
        <div style='font-family:Share Tech Mono;font-size:13px;color:#86efac;letter-spacing:3px;'>MELLOWTECH REWARDS CARD</div>
        <div style='font-size:48px;font-weight:900;color:#4ade80;margin:8px 0;font-family:Share Tech Mono;'>{pts} pts</div>
        <div style='color:#22c55e;font-size:15px;'>Card Holder: {st.session_state.username}</div>
        <div style='color:#64748b;font-size:12px;margin-top:4px;'>{dt.now().strftime("%B %Y")} · ACTIVE</div>
    </div>""", unsafe_allow_html=True)

    rewards = [
        ("⛽ Fuel Voucher R10",          50,  "Discount at any fuel station",         "#f59e0b"),
        ("⛽ 10% Petrol Discount",       120, "10% off your next full tank",           "#f59e0b"),
        ("🛒 Shopping Voucher R50",      100, "Redeem at partner stores",              "#38bdf8"),
        ("🚌 Public Transport — 5 Trips", 80, "Bus or taxi credit",                    "#22c55e"),
        ("🔧 Free Vehicle Emission Check",200, "OBD diagnostic + emission test",       "#a78bfa"),
        ("🌱 Plant a Tree",              30,  "A tree is planted in your name",        "#22c55e"),
        ("🎟️ Partner Store Discounts",   60,  "Discounts at eco-friendly shops",       "#38bdf8"),
        ("🏅 Premium Status",           500,  "Unlock extra points + top leaderboard", "#f59e0b"),
    ]

    cols = st.columns(2)
    for i, (name, cost, desc, color) in enumerate(rewards):
        can = pts >= cost
        with cols[i % 2]:
            st.markdown(f"""<div style='background:#0a0f1e;border:1px solid {"#1e293b" if not can else color+"55"};
                            border-radius:14px;padding:18px;margin-bottom:12px;
                            {"opacity:0.5;" if not can else ""}'>
                <div style='font-size:17px;font-weight:700;color:{"white" if can else "#334155"};'>{name}</div>
                <div style='color:#64748b;font-size:13px;margin:6px 0;'>{desc}</div>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-top:10px;'>
                    <span style='color:{color};font-weight:900;font-family:Share Tech Mono;font-size:22px;'>{cost} pts</span>
                    <span style='padding:8px 18px;border-radius:20px;font-size:13px;font-weight:700;
                                 background:{color+"22" if can else "#0a0f1e"};
                                 border:1px solid {color+"55" if can else "#1e293b"};
                                 color:{color if can else "#334155"};'>
                        {"✅ REDEEM" if can else "🔒 LOCKED"}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)
    st.subheader("🌿 How to Earn Green Points")
    tips = [
        ("🗺️ Use Clean Route",     "+15 pts"),
        ("🚗 Steady Speed",        "+5 pts"),
        ("🚌 Public Transport",    "+20 pts"),
        ("🚫 No Idling",           "+3 pts"),
        ("🤝 Carpool",             "+25 pts"),
        ("🔧 Service Vehicle",     "+50 pts"),
    ]
    tc = st.columns(3)
    for i, (tip, earn) in enumerate(tips):
        with tc[i % 3]:
            st.markdown(f"""<div style='background:#071a0e;border:1px solid #14532d;border-radius:12px;
                            padding:16px;margin-bottom:10px;text-align:center;'>
                <div style='font-size:15px;font-weight:700;color:#4ade80;'>{tip}</div>
                <div style='color:#22c55e;font-size:22px;font-weight:900;font-family:Share Tech Mono;margin-top:6px;'>{earn}</div>
            </div>""", unsafe_allow_html=True)


# ================================================
# PROFILE
# ================================================
elif page == "Profile":

    page_header("👤", "Profile", "#38bdf8", "Your driver profile & settings")

    c1, c2 = st.columns([1, 2])
    score  = st.session_state.eco_score
    grade  = "A" if score >= 80 else ("B" if score >= 65 else ("C" if score >= 50 else "D"))
    g_col  = "#22c55e" if score >= 80 else ("#4ade80" if score >= 65 else ("#f59e0b" if score >= 50 else "#ef4444"))

    with c1:
        st.markdown(f"""<div class='big-card' style='text-align:center;padding:28px;'>
            <div style='font-size:60px;'>🌿</div>
            <div style='font-size:22px;font-weight:900;color:#22c55e;margin-top:8px;'>{st.session_state.username}</div>
            <div class='badge' style='margin-top:8px;'>ECO DRIVER · GRADE {grade}</div>
            <hr style='border-color:#1e293b;margin:16px 0;'>
            <div style='font-size:32px;font-weight:900;color:{g_col};font-family:Share Tech Mono;'>{score}/100</div>
            <div style='color:#64748b;font-size:12px;letter-spacing:2px;'>ECO SCORE</div>
            <div style='font-size:28px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;margin-top:12px;'>{st.session_state.green_points}</div>
            <div style='color:#64748b;font-size:12px;letter-spacing:2px;'>GREEN POINTS</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.subheader("⚙️ Settings")
        new_name  = st.text_input("Your Name", value=st.session_state.username)
        home_loc  = st.selectbox("🏠 Home Location", list(locations_coords.keys()),
                                 index=list(locations_coords.keys()).index(st.session_state.home_location))
        mode      = st.selectbox("🚗 Driving Mode", ["Eco Mode 🌿", "Normal Mode", "Fast Mode ⚡"])
        alerts_on = st.toggle("🔔 Emission Alerts", value=True)
        pub_t     = st.toggle("🚌 Show Public Transport Options", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Settings", use_container_width=True):
            st.session_state.username      = new_name
            st.session_state.home_location = home_loc
            st.success("✅ Settings saved!")
            time.sleep(0.3)
            st.rerun()

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)
    st.subheader("🌍 My Climate Impact")
    co2_t = round(st.session_state.green_points * 0.12, 2)
    fuel_t = round(st.session_state.green_points * 0.05, 2)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("CO₂ Saved",       f"{co2_t} kg")
    mc2.metric("Fuel Saved",      f"{fuel_t} L")
    mc3.metric("Money Saved",     f"R{round(fuel_t*22,2)}")
    mc4.metric("Clean Trips",     st.session_state.trips_today)

    st.markdown("""<div class='banner-green' style='margin-top:16px;'>
        🌍 <b style='color:#22c55e;'>Every clean trip you make helps reduce South Africa's air pollution and slows climate change.</b>
        <span style='color:#86efac;'> Keep earning Green Points and inspiring others to drive smarter.</span>
    </div>""", unsafe_allow_html=True)
