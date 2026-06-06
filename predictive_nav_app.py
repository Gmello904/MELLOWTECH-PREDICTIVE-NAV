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
    with st.spinner("Initialising MellowTech AI..."):
        time.sleep(0.8)
    st.session_state.loaded = True

# ------------------------------------------------
# SVG ICONS (drawn, not emoji)
# ------------------------------------------------
ICONS = {
    "dashboard": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>""",
    "routes": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M6 8.5v2a4 4 0 0 0 4 4h4a4 4 0 0 1 4 4v1.5"/><path d="M6 8.5v7"/></svg>""",
    "alerts": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    "analytics": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>""",
    "score": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>""",
    "rewards": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5" rx="1"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>""",
    "profile": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>""",
    "logout": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>""",
    "leaf": """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>""",
}

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

* { font-family: 'Exo 2', sans-serif; box-sizing: border-box; }
.stApp { background: var(--bg0); color: var(--text); }
#MainMenu, footer, header { visibility: hidden; }

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #080d1a !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

div[role="radiogroup"] { gap: 2px; }
div[role="radiogroup"] > label {
    padding: 0 !important; margin: 0 !important;
    background: transparent !important; border: none !important;
}
div[role="radiogroup"] > label > div:first-child { display: none !important; }

.nav-item {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 20px; border-radius: 10px; margin: 2px 8px;
    color: #64748b; font-size: 14px; font-weight: 600;
    transition: all 0.15s; letter-spacing: 0.3px;
}
.nav-item svg { width: 18px; height: 18px; flex-shrink: 0; }
.nav-item.active {
    background: linear-gradient(90deg, #0d2318, #0a1f14);
    color: var(--green2); border-left: 3px solid var(--green); padding-left: 17px;
}

/* TITLE */
.mt-title { font-size: 44px; font-weight: 900; color: var(--green2); text-shadow: 0 0 30px #22c55e88; letter-spacing: 3px; text-align: center; line-height: 1; }
.mt-sub   { text-align: center; color: var(--muted); font-size: 12px; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 28px; }

/* CARDS */
.card { background: linear-gradient(135deg, var(--bg1), var(--bg2)); border: 1px solid var(--border); border-radius: 16px; padding: 20px; position: relative; overflow: hidden; }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--green), transparent); }
.card-red::before   { background: linear-gradient(90deg, transparent, var(--red), transparent); }
.card-amber::before { background: linear-gradient(90deg, transparent, var(--amber), transparent); }
.card-blue::before  { background: linear-gradient(90deg, transparent, var(--blue), transparent); }

.kv { font-size: 32px; font-weight: 900; font-family: 'Share Tech Mono', monospace; }
.kv-green { color: var(--green2); text-shadow: 0 0 15px #22c55e66; }
.kv-red   { color: var(--red);    text-shadow: 0 0 15px #ef444466; }
.kv-amber { color: var(--amber);  text-shadow: 0 0 15px #f59e0b66; }
.kv-blue  { color: var(--blue);   text-shadow: 0 0 15px #38bdf866; }
.kl { font-size: 11px; letter-spacing: 3px; color: var(--muted); text-transform: uppercase; margin-top: 4px; }

/* ALERTS */
.alert-red   { background:#1c0a0a; border:1px solid #7f1d1d; border-left:4px solid var(--red);   border-radius:12px; padding:16px 20px; margin:10px 0; }
.alert-green { background:#071a0e; border:1px solid #14532d; border-left:4px solid var(--green); border-radius:12px; padding:16px 20px; margin:10px 0; }
.alert-amber { background:#1a1203; border:1px solid #78350f; border-left:4px solid var(--amber); border-radius:12px; padding:16px 20px; margin:10px 0; }

/* ROUTES */
.route-red  { background:#1c0a0a; border:2px solid #ef4444; border-radius:14px; padding:18px; }
.route-blue { background:#071520; border:2px solid #38bdf8; border-radius:14px; padding:18px; }

/* PROGRESS BAR */
.pbar-bg   { background:var(--border); border-radius:20px; height:8px; margin:8px 0; }
.pbar-fill { height:8px; border-radius:20px; }

/* BADGE */
.badge { display:inline-block; background:#0d2318; color:var(--green2); border:1px solid #166534; border-radius:20px; padding:4px 14px; font-size:11px; letter-spacing:2px; }
.sep { border:none; border-top:1px solid var(--border); margin:24px 0; }

/* TEXT INPUTS */
.stTextInput > div > div > input { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; color: white !important; }
.stSelectbox > div > div { background: var(--bg2) !important; border-radius: 10px !important; }

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #14532d, #166534) !important;
    color: #4ade80 !important; border: 1px solid #166534 !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-family: 'Exo 2' !important; letter-spacing: 1px !important;
}
.stButton > button:hover { box-shadow: 0 0 20px #22c55e44 !important; }

/* LOGIN */
.login-wrap { max-width:420px; margin:50px auto; background:var(--bg1); border:1px solid var(--border); border-radius:24px; padding:44px; text-align:center; }

div[data-testid="stMetricValue"] { color: var(--green2) !important; font-family: 'Share Tech Mono' !important; }
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
        st.markdown("<h3 style='color:#22c55e;font-weight:900;margin-bottom:4px;'>Sign In</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569;font-size:12px;letter-spacing:2px;'>PROTECTING THE PLANET, ONE TRIP AT A TIME</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Your name")
        password = st.text_input("Password", type="password", placeholder="Password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Launch MellowTech", use_container_width=True):
            if not username.strip():
                st.error("Please enter a username.")
            elif not password:
                st.error("Please enter a password.")
            else:
                st.session_state.logged_in = True
                st.session_state.username  = username.strip()
                st.success(f"Welcome, {username}! Let's drive cleaner")
                time.sleep(0.5)
                st.rerun()
        st.markdown("<p style='color:#334155;font-size:11px;margin-top:16px;'>Demo: any username + any password</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ================================================
# SIDEBAR — SVG icon nav
# ================================================
NAV_ITEMS = [
    ("Dashboard",       "dashboard"),
    ("Smart Routes",    "routes"),
    ("Emission Alerts", "alerts"),
    ("Analytics",       "analytics"),
    ("Eco Score",       "score"),
    ("Rewards",         "rewards"),
    ("Profile",         "profile"),
]

with st.sidebar:
    st.markdown(f"""
    <div style='padding:24px 20px 16px;border-bottom:1px solid var(--border);'>
      <div style='display:flex;align-items:center;gap:10px;'>
        <div style='color:#22c55e;width:28px;height:28px;'>{ICONS["leaf"]}</div>
        <div>
          <div style='color:#22c55e;font-size:18px;font-weight:900;letter-spacing:3px;line-height:1;'>MELLOWTECH</div>
          <div style='color:#334155;font-size:9px;letter-spacing:2px;'>EMISSION INTELLIGENCE</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='padding:12px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;'>
      <div style='width:34px;height:34px;background:#0d2318;border:1px solid #166534;border-radius:50%;
                  display:flex;align-items:center;justify-content:center;color:#22c55e;flex-shrink:0;'>
        {ICONS["profile"]}
      </div>
      <div>
        <div style='color:#e2e8f0;font-size:13px;font-weight:600;'>{st.session_state.username}</div>
        <div style='color:#22c55e;font-size:11px;'>{st.session_state.green_points} Green Points</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:8px 0;'>", unsafe_allow_html=True)

    nav_labels = [item[0] for item in NAV_ITEMS]
    menu_choice = st.radio("", nav_labels, key="main_nav", label_visibility="collapsed")
    active_idx  = nav_labels.index(menu_choice)

    nav_html = ""
    for i, (label, icon_key) in enumerate(NAV_ITEMS):
        active_cls = "active" if i == active_idx else ""
        nav_html += f"""
        <div class='nav-item {active_cls}' style='pointer-events:none;'>
          <div style='width:18px;height:18px;flex-shrink:0;'>{ICONS[icon_key]}</div>
          <span>{label}</span>
        </div>"""

    st.markdown(f"""
    <style>
    div[role="radiogroup"] > label {{ position:relative; display:block; margin:2px 0 !important; }}
    div[role="radiogroup"] > label > div:last-child {{ opacity:0; position:absolute; top:0; left:0; right:0; bottom:0; height:44px; }}
    </style>
    <div style='position:relative;margin-top:-{len(NAV_ITEMS)*46}px;pointer-events:none;z-index:1;'>
    {nav_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='position:absolute;bottom:0;left:0;right:0;padding:16px;border-top:1px solid var(--border);background:#080d1a;'>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True, key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

menu = menu_choice


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
    if cong > 65: return "HIGH",   "#ef4444", "HIGH"
    if cong > 40: return "MEDIUM", "#f59e0b", "MED"
    return "LOW", "#22c55e", "LOW"

def page_header(icon_key, title, subtitle, color="#e2e8f0"):
    return f"""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:8px;'>
      <div style='width:32px;height:32px;color:{color};'>{ICONS[icon_key]}</div>
      <div>
        <h1 style='color:#e2e8f0;font-weight:900;margin:0;font-size:28px;'>{title}</h1>
        <p style='color:#475569;font-size:13px;margin:0;'>{subtitle}</p>
      </div>
    </div>
    <hr class='sep' style='margin-top:12px;margin-bottom:20px;'>
    """


# ================================================
# DASHBOARD
# ================================================
if menu == "Dashboard":
    st.markdown(page_header("dashboard", "Dashboard", "Live emission intelligence overview", "#22c55e"), unsafe_allow_html=True)

    time_str = dt.now().strftime("%H:%M")
    date_str = dt.now().strftime("%d %b %Y")
    rush_str = "RUSH HOUR" if is_rush else "TRAFFIC CLEAR"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='card card-blue'><div class='kv kv-blue'>{time_str}</div><div class='kl'>{date_str}</div></div>""", unsafe_allow_html=True)
    with c2:
        card_cls = "card-red" if is_rush else "card"
        kv_cls   = "kv-red"   if is_rush else "kv-green"
        st.markdown(f"""<div class='card {card_cls}'><div class='kv {kv_cls}'>{rush_str}</div><div class='kl'>TRAFFIC STATUS</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='card'><div class='kv kv-green'>{st.session_state.eco_score}/100</div><div class='kl'>ECO SCORE</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='card'><div class='kv kv-green'>{st.session_state.green_points}</div><div class='kl'>GREEN POINTS</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if is_rush:
        st.markdown("""<div class='alert-red'><b style='color:#ef4444;font-size:16px;'>HIGH EMISSION ALERT</b><br>
            <span style='color:#fca5a5;font-size:14px;'>Rush hour detected — Consider delaying your trip or choosing a clean route.</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class='alert-green'><b style='color:#22c55e;font-size:16px;'>LOW EMISSION CONDITIONS</b><br>
            <span style='color:#86efac;font-size:14px;'>Traffic is clear — great time to travel and earn Green Points.</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Real-Time City Emission Pulse</h3>", unsafe_allow_html=True)
        locs  = list(locations_coords.keys())
        congs = [congestion_for(i * 7, hour_now) for i in range(len(locs))]
        pulse = pd.DataFrame({"Zone": locs, "Emission Level %": congs})
        st.bar_chart(pulse.set_index("Zone"))

    with col_right:
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Today's Impact</h3>", unsafe_allow_html=True)
        savings_co2 = round(st.session_state.green_points * 0.12, 2)
        fuel_saved  = round(st.session_state.green_points * 0.05, 2)
        trips       = st.session_state.trips_today
        st.markdown(f"""<div class='card' style='margin-bottom:12px;'><div class='kv kv-green'>{savings_co2} kg</div><div class='kl'>CO2 Saved Today</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class='card card-amber' style='margin-bottom:12px;'><div class='kv kv-amber'>R{fuel_saved}</div><div class='kl'>Fuel Cost Saved</div></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class='card card-blue'><div class='kv kv-blue'>{trips}</div><div class='kl'>Trips Completed</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)
    st.markdown("""<div class='alert-green'><b style='color:#22c55e;'>Why It Matters</b><br>
        <span style='color:#86efac;font-size:14px;'>Vehicle emissions are a leading cause of urban air pollution. Every clean trip earns Green Points you can redeem for real rewards.</span></div>""", unsafe_allow_html=True)


# ================================================
# SMART ROUTES
# ================================================
elif menu == "Smart Routes":
    st.markdown(page_header("routes", "Smart Route Intelligence", "Choose cleaner routes — reduce emissions, earn Green Points", "#38bdf8"), unsafe_allow_html=True)

    locs = list(locations_coords.keys())
    c1, c2, c3 = st.columns(3)
    with c1: origin = st.selectbox("Origin", locs)
    with c2: dest   = st.selectbox("Destination", [l for l in locs if l != origin])
    with c3: leave  = st.slider("Departure Hour", 0, 23, hour_now)

    waypoints = st.multiselect("Add Waypoints (optional)", [l for l in locs if l not in [origin, dest]])
    st.markdown("<br>", unsafe_allow_html=True)

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
            <div style='font-size:16px;font-weight:800;color:#38bdf8;'>CLEAN ROUTE — RECOMMENDED</div>
            <div style='color:#7dd3fc;font-size:11px;letter-spacing:2px;margin-bottom:16px;'>LOW EMISSIONS · LESS TRAFFIC</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>
                <div><div style='font-size:26px;font-weight:900;color:#38bdf8;font-family:Share Tech Mono;'>{cong_a}%</div><div style='color:#64748b;font-size:11px;'>CONGESTION</div></div>
                <div><div style='font-size:26px;font-weight:900;color:#38bdf8;font-family:Share Tech Mono;'>{time_a} min</div><div style='color:#64748b;font-size:11px;'>TRAVEL TIME</div></div>
                <div><div style='font-size:26px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{dist_a} km</div><div style='color:#64748b;font-size:11px;'>DISTANCE</div></div>
                <div><div style='font-size:26px;font-weight:900;color:#4ade80;font-family:Share Tech Mono;'>{co2_a} kg</div><div style='color:#64748b;font-size:11px;'>CO2 EMITTED</div></div>
            </div>
            <div style='margin-top:14px;background:#0a1a2e;border-radius:8px;padding:10px;font-size:13px;color:#7dd3fc;'>
                Smooth flow · Lower fuel burn · Earn +15 Green Points
            </div>
        </div>""", unsafe_allow_html=True)

    with colB:
        st.markdown(f"""<div class='route-red'>
            <div style='font-size:16px;font-weight:800;color:#ef4444;'>HIGH EMISSION ROUTE — AVOID</div>
            <div style='color:#fca5a5;font-size:11px;letter-spacing:2px;margin-bottom:16px;'>HEAVY TRAFFIC · MORE FUEL</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;'>
                <div><div style='font-size:26px;font-weight:900;color:#ef4444;font-family:Share Tech Mono;'>{cong_b}%</div><div style='color:#64748b;font-size:11px;'>CONGESTION</div></div>
                <div><div style='font-size:26px;font-weight:900;color:#ef4444;font-family:Share Tech Mono;'>{time_b} min</div><div style='color:#64748b;font-size:11px;'>TRAVEL TIME</div></div>
                <div><div style='font-size:26px;font-weight:900;color:#f87171;font-family:Share Tech Mono;'>{dist_b} km</div><div style='color:#64748b;font-size:11px;'>DISTANCE</div></div>
                <div><div style='font-size:26px;font-weight:900;color:#f87171;font-family:Share Tech Mono;'>{co2_b} kg</div><div style='color:#64748b;font-size:11px;'>CO2 EMITTED</div></div>
            </div>
            <div style='margin-top:14px;background:#1c0808;border-radius:8px;padding:10px;font-size:13px;color:#fca5a5;'>
                Stop-and-go traffic · High idling · Increased fuel burn
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div class='alert-green'><b style='color:#22c55e;'>Smart Advisor</b><br>
        <span style='color:#86efac;font-size:14px;'>Taking the Clean Route saves <b>{round(co2_b - co2_a, 2)} kg CO2</b> and
        approximately <b>R{round((fuel_b - fuel_a)*20, 2)}</b> in fuel. You will earn <b>+15 Green Points</b>.</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Take Clean Route — Start Trip", use_container_width=True):
        st.session_state.green_points += 15
        st.session_state.trips_today  += 1
        st.session_state.eco_score     = min(100, st.session_state.eco_score + 1)
        st.success(f"Trip started! +15 Green Points added. Total: {st.session_state.green_points} pts")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Route Map</h3>", unsafe_allow_html=True)
    route     = [origin] + waypoints + [dest]
    route_pts = [locations_coords[r] for r in route]
    map_df    = pd.DataFrame(route_pts, columns=["lat", "lon"])
    st.map(map_df, zoom=12)
    for i, stop in enumerate(route):
        marker = "Start" if i == 0 else ("End" if i == len(route)-1 else "Stop")
        st.markdown(f"**{marker}:** {stop}")


# ================================================
# EMISSION ALERTS
# ================================================
elif menu == "Emission Alerts":
    st.markdown(page_header("alerts", "Emission Alerts", "Live diagnostics and driving behaviour intelligence", "#ef4444"), unsafe_allow_html=True)

    np.random.seed(hour_now * 3)
    emission_pct = np.random.randint(20, 95) if is_rush else np.random.randint(10, 55)
    speed_kmh    = np.random.randint(15, 45) if is_rush else np.random.randint(50, 100)
    idle_mins    = np.random.randint(0, 8)
    rpm          = np.random.randint(800, 4000)

    if emission_pct > 65:
        st.markdown(f"""<div class='alert-red'>
            <div style='font-size:18px;font-weight:900;color:#ef4444;'>HIGH EMISSION DETECTED</div>
            <div style='color:#fca5a5;margin-top:6px;font-size:14px;'>Your vehicle is producing above-normal emissions. Reduce speed and check engine diagnostics.</div>
        </div>""", unsafe_allow_html=True)
    elif emission_pct > 40:
        st.markdown(f"""<div class='alert-amber'>
            <div style='font-size:18px;font-weight:900;color:#f59e0b;'>MODERATE EMISSIONS</div>
            <div style='color:#fde68a;margin-top:6px;font-size:14px;'>Emissions slightly elevated — maintain steady speed and avoid sudden braking.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='alert-green'>
            <div style='font-size:18px;font-weight:900;color:#22c55e;'>LOW EMISSIONS — CLEAN DRIVING</div>
            <div style='color:#86efac;margin-top:6px;font-size:14px;'>Excellent! Your vehicle is running efficiently. Keep it up and earn Green Points.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    em_card = "card-red" if emission_pct > 65 else ("card-amber" if emission_pct > 40 else "card")
    em_kv   = "kv-red"   if emission_pct > 65 else ("kv-amber"   if emission_pct > 40 else "kv-green")
    with c1: st.markdown(f"""<div class='card {em_card}'><div class='kv {em_kv}'>{emission_pct}%</div><div class='kl'>EMISSION LEVEL</div></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class='card card-blue'><div class='kv kv-blue'>{speed_kmh} km/h</div><div class='kl'>CURRENT SPEED</div></div>""", unsafe_allow_html=True)
    with c3:
        idle_card = "card-amber" if idle_mins > 2 else "card"
        idle_kv   = "kv-amber"   if idle_mins > 2 else "kv-green"
        st.markdown(f"""<div class='card {idle_card}'><div class='kv {idle_kv}'>{idle_mins} min</div><div class='kl'>IDLE TIME</div></div>""", unsafe_allow_html=True)
    with c4:
        rpm_card = "card-red" if rpm > 3000 else "card"
        rpm_kv   = "kv-red"   if rpm > 3000 else "kv-green"
        st.markdown(f"""<div class='card {rpm_card}'><div class='kv {rpm_kv}'>{rpm}</div><div class='kl'>ENGINE RPM</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:4px;'>Speed & Emission Relationship</h3>", unsafe_allow_html=True)
    speeds   = list(range(0, 130, 10))
    em_curve = [85, 80, 70, 55, 38, 25, 20, 18, 22, 30, 42, 58, 75]
    st.line_chart(pd.DataFrame({"Speed (km/h)": speeds, "Relative Emission %": em_curve}).set_index("Speed (km/h)"))

    st.markdown("""<div class='alert-green'><b style='color:#22c55e;'>Key Insight</b>
        <span style='color:#86efac;font-size:14px;'> Driving at a steady 60-80 km/h produces the least pollution. Stop-and-go and speeding above 100 km/h burn significantly more fuel.</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Action Plan</h3>", unsafe_allow_html=True)
    actions = [
        ("Check Engine Diagnostics",   "Run an OBD scan or visit a mechanic if emissions remain high.", "#ef4444"),
        ("Reduce Fuel Waste",          "Avoid rapid acceleration, maintain 60-80 km/h, reduce RPM, coast to slow down.", "#f59e0b"),
        ("Service Your Vehicle",       "Oil change, air filter, fuel injector cleaning, exhaust system check.", "#38bdf8"),
        ("Stop Unnecessary Idling",    "Switch off engine after 1 minute of idling to prevent fuel waste.", "#f59e0b"),
        ("Switch to a Cleaner Route",  "Less traffic means less emissions. Open Smart Routes for alternatives.", "#22c55e"),
    ]
    for title, desc, color in actions:
        st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-left:3px solid {color};border-radius:10px;padding:14px;margin-bottom:8px;'>
            <div style='color:{color};font-weight:700;font-size:15px;'>{title}</div>
            <div style='color:#94a3b8;font-size:13px;margin-top:4px;'>{desc}</div>
        </div>""", unsafe_allow_html=True)


# ================================================
# ANALYTICS
# ================================================
elif menu == "Analytics":
    st.markdown(page_header("analytics", "Analytics", "Traffic and emission trends, zone status, cost impact", "#38bdf8"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Hourly Trends", "Zone Emissions", "Cost Impact", "Weekly Heatmap"])

    with tab1:
        hours = list(range(24))
        np.random.seed(5)
        base_em   = np.random.randint(15, 50, 24).tolist()
        emissions = [min(100, e + 35 if 7 <= h <= 9 or 16 <= h <= 18 else e) for e, h in zip(base_em, hours)]
        speeds    = [max(10, 85 - em // 2 + np.random.randint(-5, 5)) for em in emissions]
        fuel_burn = [round(em * 0.08 + np.random.uniform(0, 2), 1) for em in emissions]
        df_hourly = pd.DataFrame({"Hour": hours, "Emission %": emissions, "Avg Speed km/h": speeds, "Fuel L/100km": fuel_burn}).set_index("Hour")
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>24-Hour Emission & Speed Trends</h3>", unsafe_allow_html=True)
        st.line_chart(df_hourly)
        peak_h = hours[np.argmax(emissions)]
        st.warning(f"Peak emissions at **{peak_h}:00** ({max(emissions)}%) — morning/evening rush hour.")
        st.success("Cleanest travel window: **10:00-15:00** and **20:00-06:00**")

    with tab2:
        locs  = list(locations_coords.keys())
        np.random.seed(33)
        congs = [congestion_for(i * 11, hour_now) for i in range(len(locs))]
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Zone Emission Status</h3>", unsafe_allow_html=True)
        for i, loc in enumerate(locs):
            lvl, col, _ = emission_level(congs[i])
            pct = congs[i]
            st.markdown(f"""<div style='background:#0a0f1e;border:1px solid #1e293b;border-radius:10px;padding:14px;margin-bottom:8px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-weight:700;font-size:15px;'>{loc}</span>
                    <span style='background:{col}22;color:{col};border:1px solid {col}55;border-radius:20px;padding:3px 12px;font-size:11px;font-weight:700;'>{lvl}</span>
                </div>
                <div class='pbar-bg'><div class='pbar-fill' style='width:{pct}%;background:{col};'></div></div>
                <div style='color:#64748b;font-size:12px;'>{pct}% congestion</div>
            </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Fuel Cost Impact Estimator</h3>", unsafe_allow_html=True)
        weekly_km   = st.slider("Weekly driving distance (km)", 50, 500, 200)
        fuel_price  = st.slider("Fuel price (R/litre)", 18, 26, 22)
        drive_style = st.selectbox("Driving style", ["Aggressive (stop-and-go)", "Moderate (steady speed)", "Eco (smooth & efficient)"])
        consumption = {"Aggressive (stop-and-go)": 12, "Moderate (steady speed)": 8, "Eco (smooth & efficient)": 6}
        litres_week = weekly_km / 100 * consumption[drive_style]
        cost_week   = round(litres_week * fuel_price, 2)
        cost_month  = round(cost_week * 4.3, 2)
        co2_week    = round(litres_week * 2.31, 2)
        eco_litres  = weekly_km / 100 * 6
        eco_cost    = round(eco_litres * fuel_price, 2)
        saving      = round(cost_week - eco_cost, 2)
        ca, cb, cc, cd = st.columns(4)
        ca.metric("Weekly Fuel Cost", f"R{cost_week}")
        cb.metric("Monthly Fuel Cost", f"R{cost_month}")
        cc.metric("CO2 per Week", f"{co2_week} kg")
        cd.metric("Potential Weekly Saving", f"R{max(0, saving)}")
        if saving > 0:
            st.markdown(f"""<div class='alert-amber'><b style='color:#f59e0b;'>Cost Intelligence</b>
                <span style='color:#fde68a;font-size:14px;'> Switching to Eco driving could save you <b>R{saving}/week</b> (R{round(saving*52, 0)}/year).</span></div>""", unsafe_allow_html=True)

    with tab4:
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        hrs  = list(range(6, 21))
        np.random.seed(42)
        heat = np.random.randint(10, 80, (7, len(hrs)))
        for i in range(7):
            for j, h in enumerate(hrs):
                if h in [7, 8, 17, 18] and i < 5:
                    heat[i][j] = min(100, heat[i][j] + 35)
        heat_df = pd.DataFrame(heat, index=days, columns=[f"{h}:00" for h in hrs])
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Weekly Emission Heatmap</h3>", unsafe_allow_html=True)
        st.dataframe(heat_df.style.background_gradient(cmap="RdYlGn_r"), use_container_width=True)
        st.caption("Red = heavy congestion + high emissions  ·  Green = smooth flow + low emissions")


# ================================================
# ECO SCORE
# ================================================
elif menu == "Eco Score":
    st.markdown(page_header("score", "Eco Score", "Your environmental driving rating", "#22c55e"), unsafe_allow_html=True)

    score = st.session_state.eco_score
    if score >= 80:   grade, grade_col, grade_label = "A", "#22c55e", "Excellent Eco Driver"
    elif score >= 65: grade, grade_col, grade_label = "B", "#4ade80", "Good Eco Driver"
    elif score >= 50: grade, grade_col, grade_label = "C", "#f59e0b", "Average Driver"
    else:             grade, grade_col, grade_label = "D", "#ef4444", "High Emission Driver"

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""<div class='card' style='text-align:center;padding:30px;'>
            <div style='font-size:80px;font-weight:900;color:{grade_col};font-family:Share Tech Mono;text-shadow:0 0 30px {grade_col}88;'>{grade}</div>
            <div style='font-size:40px;font-weight:900;color:{grade_col};font-family:Share Tech Mono;'>{score}/100</div>
            <div style='color:#64748b;font-size:11px;letter-spacing:2px;margin-top:8px;'>{grade_label.upper()}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Weekly Performance</h3>", unsafe_allow_html=True)
        weeks   = ["6 wks ago","5 wks ago","4 wks ago","3 wks ago","2 wks ago","Last week","This week"]
        scores  = st.session_state.weekly_scores
        week_df = pd.DataFrame({"Week": weeks, "Eco Score": scores})
        st.line_chart(week_df.set_index("Week"))
        trend = scores[-1] - scores[-2]
        if trend > 0:   st.success(f"Improving! +{trend} points vs last week.")
        elif trend < 0: st.warning(f"Score dropped {abs(trend)} points. Try choosing cleaner routes.")
        else:           st.info("Score stable this week.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Score Breakdown</h3>", unsafe_allow_html=True)
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
                <span style='color:{color};font-weight:700;'>{val}/100</span>
            </div>
            <div class='pbar-bg'><div class='pbar-fill' style='width:{val}%;background:{color};'></div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Driver Leaderboard</h3>", unsafe_allow_html=True)
    lb_data = {
        "Rank": ["1st","2nd","3rd","4th","5th"],
        "Driver": ["EcoDriver_01","GreenWheels","CleanCommuter", st.session_state.username, "QuickRacer"],
        "Eco Score": [96, 91, 88, score, 43],
        "Green Points": [1240, 985, 872, st.session_state.green_points, 120],
        "CO2 Saved (kg)": [148, 118, 104, round(st.session_state.green_points * 0.12, 1), 14],
    }
    st.dataframe(pd.DataFrame(lb_data), use_container_width=True, hide_index=True)


# ================================================
# REWARDS
# ================================================
elif menu == "Rewards":
    st.markdown(page_header("rewards", "Rewards", "Convert your Green Points into real-world rewards", "#f59e0b"), unsafe_allow_html=True)

    pts = st.session_state.green_points
    st.markdown(f"""<div style='background:linear-gradient(135deg,#0f2a0a,#1a3a10);border:1px solid #166534;border-radius:20px;padding:28px;margin-bottom:24px;position:relative;overflow:hidden;'>
        <div style='font-family:Share Tech Mono;font-size:11px;color:#86efac;letter-spacing:3px;'>MELLOWTECH REWARDS CARD</div>
        <div style='font-size:42px;font-weight:900;color:#4ade80;margin:8px 0;font-family:Share Tech Mono;'>{pts} pts</div>
        <div style='color:#22c55e;font-size:14px;'>{st.session_state.username}</div>
        <div style='color:#64748b;font-size:12px;margin-top:4px;'>{dt.now().strftime("%B %Y")} · ACTIVE</div>
    </div>""", unsafe_allow_html=True)

    rewards = [
        ("Fuel Voucher",            50,  "Save R10 at participating fuel stations",  "#f59e0b"),
        ("Petrol Discount 10%",     120, "10% off your next full tank",              "#f59e0b"),
        ("Shopping Voucher R50",    100, "Redeem at partner retailers",              "#38bdf8"),
        ("Public Transport Credit", 80,  "Bus or taxi credit for 5 trips",           "#22c55e"),
        ("Free Vehicle Check",      200, "Emission diagnostic + engine check",       "#a78bfa"),
        ("Tree Planting Credit",    30,  "Sponsor a tree planted in your name",      "#22c55e"),
        ("Partner Discounts",       60,  "Discounts at eco-friendly stores",         "#38bdf8"),
        ("Premium Eco Status",      500, "Unlock premium leaderboard + extra points","#f59e0b"),
    ]
    cols = st.columns(2)
    for i, (name, cost, desc, color) in enumerate(rewards):
        with cols[i % 2]:
            can_afford = pts >= cost
            lock_text  = "Tap to Redeem" if can_afford else f"Need {cost - pts} more pts"
            lock_col   = color if can_afford else "#334155"
            border_col = color + "44" if can_afford else "#1e293b"
            st.markdown(f"""<div style='background:#0a0f1e;border:1px solid {border_col};border-radius:14px;padding:16px;margin-bottom:12px;'>
                <div style='font-size:15px;font-weight:700;color:{"#e2e8f0" if can_afford else "#334155"};'>{name}</div>
                <div style='color:#64748b;font-size:13px;margin:4px 0;'>{desc}</div>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-top:10px;'>
                    <span style='color:{color};font-weight:900;font-family:Share Tech Mono;font-size:18px;'>{cost} pts</span>
                    <span style='color:{lock_col};font-size:12px;font-weight:600;'>{lock_text}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>How to Earn Green Points</h3>", unsafe_allow_html=True)
    earn_tips = [
        ("Choose Clean Routes",    "+15 pts per trip"),
        ("Maintain Steady Speed",  "+5 pts per clean trip"),
        ("Use Public Transport",   "+20 pts per trip"),
        ("No Idling",              "+3 pts under 1 min idle"),
        ("Carpool / Rideshare",    "+25 pts per shared trip"),
        ("Service Your Vehicle",   "+50 pts after check-up"),
    ]
    cols2 = st.columns(3)
    for i, (tip, pts_earn) in enumerate(earn_tips):
        with cols2[i % 3]:
            st.markdown(f"""<div style='background:#071a0e;border:1px solid #14532d;border-radius:10px;padding:14px;margin-bottom:10px;text-align:center;'>
                <div style='font-size:14px;font-weight:700;color:#4ade80;'>{tip}</div>
                <div style='color:#22c55e;font-size:16px;font-weight:900;font-family:Share Tech Mono;margin-top:6px;'>{pts_earn}</div>
            </div>""", unsafe_allow_html=True)


# ================================================
# PROFILE
# ================================================
elif menu == "Profile":
    st.markdown(page_header("profile", "Profile", "Your account and preferences", "#38bdf8"), unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        score = st.session_state.eco_score
        grade = "A" if score >= 80 else ("B" if score >= 65 else ("C" if score >= 50 else "D"))
        g_col = "#22c55e" if score >= 80 else ("#4ade80" if score >= 65 else ("#f59e0b" if score >= 50 else "#ef4444"))
        st.markdown(f"""<div class='card' style='text-align:center;padding:28px;'>
            <div style='font-size:48px;'>🌿</div>
            <div style='font-size:20px;font-weight:900;color:#22c55e;margin-top:8px;'>{st.session_state.username}</div>
            <div class='badge' style='margin-top:6px;'>GRADE {grade}</div>
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
        st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>Preferences</h3>", unsafe_allow_html=True)
        new_name   = st.text_input("Display Name", value=st.session_state.username)
        home_loc   = st.selectbox("Home Location", list(locations_coords.keys()),
                                  index=list(locations_coords.keys()).index(st.session_state.home_location))
        drive_pref = st.selectbox("Default Driving Mode", ["Eco Mode", "Normal Mode", "Fast Mode"])
        notifs     = st.toggle("Enable Emission Alerts", value=True)
        pub_trans  = st.toggle("Promote Public Transport Routes", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Preferences", use_container_width=True):
            st.session_state.username      = new_name
            st.session_state.home_location = home_loc
            st.session_state.driving_mode  = drive_pref
            st.success("Preferences saved!")
            time.sleep(0.4)
            st.rerun()

    st.markdown("<hr class='sep'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e2e8f0;font-size:16px;font-weight:700;margin-bottom:12px;'>My Environmental Impact</h3>", unsafe_allow_html=True)
    co2_total   = round(st.session_state.green_points * 0.12, 2)
    fuel_total  = round(st.session_state.green_points * 0.05, 2)
    money_saved = round(fuel_total * 22, 2)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Total CO2 Saved",  f"{co2_total} kg")
    mc2.metric("Fuel Saved",       f"{fuel_total} L")
    mc3.metric("Money Saved",      f"R{money_saved}")
    mc4.metric("Trips Completed",  st.session_state.trips_today)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div class='alert-green'><b style='color:#22c55e;'>Your Climate Contribution</b><br>
        <span style='color:#86efac;font-size:14px;'>By using MellowTech, you have helped reduce urban air pollution and contributed to
        South Africa's climate goals. Every clean trip counts.</span></div>""", unsafe_allow_html=True)
