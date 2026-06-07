import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MellowTech",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;800;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
}
.main { background-color: #030712; }
.block-container { padding-top: 1.5rem; }

.mt-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    color: #4ade80;
    letter-spacing: 4px;
    text-align: center;
    margin-bottom: 0;
}
.mt-sub {
    font-size: 0.7rem;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: #475569;
    text-align: center;
    margin-bottom: 1.5rem;
}
.kpi-box {
    background: linear-gradient(135deg, #0a0f1e, #0f1929);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    margin-bottom: 8px;
}
.kpi-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #22c55e, transparent);
}
.kpi-box-red::before   { background: linear-gradient(90deg, transparent, #ef4444, transparent); }
.kpi-box-amber::before { background: linear-gradient(90deg, transparent, #f59e0b, transparent); }
.kpi-box-blue::before  { background: linear-gradient(90deg, transparent, #38bdf8, transparent); }

.kpi-val        { font-family: 'Share Tech Mono', monospace; font-size: 1.7rem; font-weight: 900; color: #4ade80; }
.kpi-val-red    { color: #ef4444; }
.kpi-val-amber  { color: #f59e0b; }
.kpi-val-blue   { color: #38bdf8; }
.kpi-lbl        { font-size: 0.62rem; letter-spacing: 3px; color: #475569; text-transform: uppercase; margin-top: 2px; }

.alert-red   { background: #1c0a0a; border: 1px solid #7f1d1d; border-left: 4px solid #ef4444; border-radius: 10px; padding: 12px 16px; margin: 8px 0; }
.alert-green { background: #071a0e; border: 1px solid #14532d; border-left: 4px solid #22c55e; border-radius: 10px; padding: 12px 16px; margin: 8px 0; }
.alert-amber { background: #1a1203; border: 1px solid #78350f; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 12px 16px; margin: 8px 0; }

.route-blue { background: #071520; border: 2px solid #38bdf8; border-radius: 12px; padding: 16px; }
.route-red  { background: #1c0a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 16px; }

.pbar-bg   { background: #1e293b; border-radius: 20px; height: 8px; margin: 5px 0; }
.pbar-fill { height: 8px; border-radius: 20px; }

.sec-head { color: #e2e8f0; font-size: 0.9rem; font-weight: 700; margin: 14px 0 8px; border-bottom: 1px solid #1e293b; padding-bottom: 4px; }

.badge { display: inline-block; background: #0d2318; color: #4ade80; border: 1px solid #166534; border-radius: 20px; padding: 2px 12px; font-size: 0.7rem; letter-spacing: 2px; }

.reward-card { background: #0a0f1e; border: 1px solid #1e293b; border-radius: 10px; padding: 12px; margin-bottom: 8px; }
.action-card { background: #0a0f1e; border: 1px solid #1e293b; border-left: 3px solid #22c55e; border-radius: 8px; padding: 12px; margin-bottom: 8px; }

.sidebar-brand { font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; font-weight: 900; color: #4ade80; letter-spacing: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── DATA & HELPERS ──────────────────────────────────────────────────────────
LOCATIONS = {
    "Home":     {"lat": -25.7461, "lon": 28.1881},
    "Work":     {"lat": -25.7580, "lon": 28.1890},
    "School":   {"lat": -25.7400, "lon": 28.2100},
    "Mall":     {"lat": -25.7650, "lon": 28.3120},
    "Hospital": {"lat": -25.7320, "lon": 28.2280},
    "Airport":  {"lat": -25.9180, "lon": 28.3820},
    "Park":     {"lat": -25.7280, "lon": 28.2450},
    "Garage":   {"lat": -25.7500, "lon": 28.1750},
}
LOC_NAMES = list(LOCATIONS.keys())

def seeded_rand(seed):
    rng = random.Random(seed)
    return rng.random

def seeded_val(seed):
    return random.Random(seed).random()

def congestion_for(seed, hr):
    r = random.Random(seed).random()
    v = int(r * 55) + 15
    if (7 <= hr <= 9) or (16 <= hr <= 18):
        v = min(100, v + 30)
    return v

def emission_level(c):
    if c > 65:
        return {"label": "HIGH",   "color": "#ef4444"}
    if c > 40:
        return {"label": "MEDIUM", "color": "#f59e0b"}
    return     {"label": "LOW",    "color": "#22c55e"}

now      = datetime.now()
HOUR     = now.hour
IS_RUSH  = (7 <= HOUR <= 9) or (16 <= HOUR <= 18)
TIME_STR = now.strftime("%H:%M")
DATE_STR = now.strftime("%d %b %Y")

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0a0f1e",
    font=dict(color="#475569", size=10),
    margin=dict(l=30, r=10, t=20, b=30),
    xaxis=dict(gridcolor="#1e293b", linecolor="#1e293b"),
    yaxis=dict(gridcolor="#1e293b", linecolor="#1e293b"),
)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "logged_in":    False,
        "username":     "",
        "green_points": 0,
        "eco_score":    72,
        "trips":        0,
        "home_loc":     "Home",
        "driving_mode": "Normal Mode",
        "weekly_scores":[55, 61, 58, 67, 70, 68, 72],
        "page":         "Dashboard",
        "trip_msg":     "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── KPI CARD HELPER ─────────────────────────────────────────────────────────
def kpi_card(value, label, color_class="", val_class="kpi-val"):
    box_cls = f"kpi-box {color_class}"
    return f"""
<div class="{box_cls}">
  <div class="{val_class}">{value}</div>
  <div class="kpi-lbl">{label}</div>
</div>"""

def kpi_cols(items, cols=4):
    columns = st.columns(cols)
    for i, (val, lbl, box_c, val_c) in enumerate(items):
        with columns[i % cols]:
            st.markdown(kpi_card(val, lbl, box_c, val_c), unsafe_allow_html=True)

# ─── LOGIN SCREEN ─────────────────────────────────────────────────────────────
def show_login():
    st.markdown('<div class="mt-title">🌿 MELLOWTECH</div>', unsafe_allow_html=True)
    st.markdown('<div class="mt-sub">Smart Emission Intelligence System</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### Sign In")
        st.caption("PROTECTING THE PLANET, ONE TRIP AT A TIME")
        username = st.text_input("Username", key="login_user", placeholder="Username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Password")
        if st.button("🚀 Launch MellowTech", use_container_width=True, type="primary"):
            if not username.strip():
                st.error("Please enter a username.")
            elif not password:
                st.error("Please enter a password.")
            else:
                st.session_state.logged_in = True
                st.session_state.username  = username.strip()
                st.rerun()
        st.caption("Demo: any username + any password")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
def show_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🌿 MELLOWTECH</div>', unsafe_allow_html=True)
        st.caption("EMISSION INTELLIGENCE")
        st.markdown("---")
        st.markdown(f"👤 **{st.session_state.username}**")
        st.markdown(f"<span style='color:#22c55e;font-size:0.85rem'>{st.session_state.green_points} Green Points</span>", unsafe_allow_html=True)

        score = st.session_state.eco_score
        st.caption("ECO SCORE")
        st.progress(score / 100)
        st.markdown(f"<span style='color:#4ade80;font-weight:700'>{score}/100</span>", unsafe_allow_html=True)
        st.markdown("---")

        nav_items = [
            ("🏠", "Dashboard"),
            ("🗺️", "Smart Routes"),
            ("⚠️", "Emission Alerts"),
            ("📊", "Analytics"),
            ("⭐", "Eco Score"),
            ("🎁", "Rewards"),
            ("👤", "Profile"),
        ]
        for icon, label in nav_items:
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.page = label
                st.rerun()

        st.markdown("---")
        if st.button("🔓 Sign Out", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ─── PAGE: DASHBOARD ─────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown("## 🏠 Dashboard")
    st.caption("Live emission intelligence overview")
    st.markdown("---")

    pulse_data = [(n, congestion_for(i * 7 + 1, HOUR)) for i, n in enumerate(LOC_NAMES)]
    savings    = round(st.session_state.green_points * 0.12, 2)
    fuel       = round(st.session_state.green_points * 0.05, 2)

    kpi_cols([
        (TIME_STR,                          DATE_STR,        "kpi-box-blue",  "kpi-val kpi-val-blue"),
        ("RUSH HOUR" if IS_RUSH else "CLEAR","TRAFFIC STATUS","kpi-box-red" if IS_RUSH else "", "kpi-val kpi-val-red" if IS_RUSH else "kpi-val"),
        (f"{st.session_state.eco_score}/100","ECO SCORE",    "",              "kpi-val"),
        (st.session_state.green_points,     "GREEN POINTS",  "",              "kpi-val"),
    ])

    if IS_RUSH:
        st.markdown('<div class="alert-red"><b style="color:#ef4444">⚠️ HIGH EMISSION ALERT</b><br><span style="color:#fca5a5;font-size:0.82rem">Rush hour — consider delaying or choosing a clean route.</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-green"><b style="color:#22c55e">✅ LOW EMISSION CONDITIONS</b><br><span style="color:#86efac;font-size:0.82rem">Traffic is clear — great time to travel and earn Green Points.</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Real-Time City Emission Pulse</div>', unsafe_allow_html=True)
    names  = [d[0] for d in pulse_data]
    values = [d[1] for d in pulse_data]
    colors = [emission_level(v)["color"] for v in values]

    fig = go.Figure(go.Bar(x=names, y=values, marker_color=colors))
    fig.update_layout(**PLOTLY_LAYOUT, height=220, yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="sec-head">Today\'s Impact</div>', unsafe_allow_html=True)
    kpi_cols([
        (f"{savings} kg",                        "CO2 SAVED TODAY",     "",             "kpi-val"),
        (f"R{fuel}",                              "FUEL COST SAVED",     "kpi-box-amber","kpi-val kpi-val-amber"),
        (st.session_state.trips,                  "TRIPS COMPLETED",     "kpi-box-blue", "kpi-val kpi-val-blue"),
        (st.session_state.green_points,           "TOTAL GREEN POINTS",  "",             "kpi-val"),
    ])

    st.markdown('<div class="alert-green"><b style="color:#22c55e">Why It Matters</b><br><span style="color:#86efac;font-size:0.82rem">Every clean trip earns Green Points redeemable for real rewards while reducing urban air pollution.</span></div>', unsafe_allow_html=True)

# ─── PAGE: SMART ROUTES ──────────────────────────────────────────────────────
def page_smart_routes():
    st.markdown("## 🗺️ Smart Routes")
    st.caption("Choose cleaner routes — reduce emissions, earn Green Points")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        origin = st.selectbox("ORIGIN", LOC_NAMES, key="sr_origin")
    with c2:
        dests = [l for l in LOC_NAMES if l != origin]
        dest  = st.selectbox("DESTINATION", dests, key="sr_dest")

    leave_hr = st.slider("DEPARTURE HOUR", 0, 23, HOUR, key="sr_hour",
                         format="%d:00")

    seed = leave_hr + ord(origin[0]) + ord(dest[0])
    rng  = random.Random(seed)
    cong_a = min(100, int(rng.random() * 35) + 10)
    cong_b = min(100, int(rng.random() * 40) + 50 + (25 if IS_RUSH else 0))
    dist_a = round(rng.random() * 14 + 4, 1)
    dist_b = round(dist_a * (rng.random() * 0.5 + 0.8), 1)
    time_a = round(dist_a * 1.5 + cong_a * 0.3)
    time_b = round(dist_b * 1.5 + cong_b * 0.5)
    fuel_a = round(dist_a * 0.08, 2)
    fuel_b = round(dist_b * 0.08 + cong_b * 0.005, 2)
    co2_a  = round(fuel_a * 2.31, 2)
    co2_b  = round(fuel_b * 2.31, 2)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
<div class="route-blue">
  <div style="font-size:0.9rem;font-weight:800;color:#38bdf8">✅ CLEAN ROUTE</div>
  <div style="color:#7dd3fc;font-size:0.65rem;letter-spacing:2px;margin-bottom:10px">LOW EMISSIONS · RECOMMENDED</div>
  <table style="width:100%;font-size:0.8rem">
    <tr><td style="color:#475569">Congestion</td><td style="font-family:monospace;color:#38bdf8;font-weight:900">{cong_a}%</td>
        <td style="color:#475569">Time</td><td style="font-family:monospace;color:#38bdf8;font-weight:900">{time_a} min</td></tr>
    <tr><td style="color:#475569">Distance</td><td style="font-family:monospace;color:#4ade80;font-weight:900">{dist_a} km</td>
        <td style="color:#475569">CO2</td><td style="font-family:monospace;color:#4ade80;font-weight:900">{co2_a} kg</td></tr>
  </table>
  <div style="margin-top:10px;background:#0a1a2e;border-radius:6px;padding:8px;font-size:0.78rem;color:#7dd3fc">
    Smooth flow · Earn +15 Green Points
  </div>
</div>""", unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
<div class="route-red">
  <div style="font-size:0.9rem;font-weight:800;color:#ef4444">⛔ HIGH EMISSION ROUTE</div>
  <div style="color:#fca5a5;font-size:0.65rem;letter-spacing:2px;margin-bottom:10px">HEAVY TRAFFIC · AVOID</div>
  <table style="width:100%;font-size:0.8rem">
    <tr><td style="color:#475569">Congestion</td><td style="font-family:monospace;color:#ef4444;font-weight:900">{cong_b}%</td>
        <td style="color:#475569">Time</td><td style="font-family:monospace;color:#ef4444;font-weight:900">{time_b} min</td></tr>
    <tr><td style="color:#475569">Distance</td><td style="font-family:monospace;color:#f87171;font-weight:900">{dist_b} km</td>
        <td style="color:#475569">CO2</td><td style="font-family:monospace;color:#f87171;font-weight:900">{co2_b} kg</td></tr>
  </table>
  <div style="margin-top:10px;background:#1c0808;border-radius:6px;padding:8px;font-size:0.78rem;color:#fca5a5">
    Stop-and-go · High idling · More fuel
  </div>
</div>""", unsafe_allow_html=True)

    co2_save  = round(co2_b - co2_a, 2)
    fuel_save = round((fuel_b - fuel_a) * 20, 2)
    st.markdown(f'<div class="alert-green" style="margin-top:12px"><b style="color:#22c55e">Smart Advisor</b><br><span style="color:#86efac;font-size:0.82rem">Taking the Clean Route saves <b>{co2_save} kg CO2</b> and ~<b>R{fuel_save}</b> in fuel. Earn <b>+15 Green Points</b>.</span></div>', unsafe_allow_html=True)

    st.markdown("")
    if st.button("🚗 Take Clean Route — Start Trip", type="primary"):
        st.session_state.green_points += 15
        st.session_state.trips        += 1
        st.session_state.eco_score     = min(100, st.session_state.eco_score + 1)
        st.success(f"✅ Trip started! +15 pts added. Total: {st.session_state.green_points} pts")
        st.rerun()

# ─── PAGE: EMISSION ALERTS ───────────────────────────────────────────────────
def page_emission_alerts():
    st.markdown("## ⚠️ Emission Alerts")
    st.caption("Live diagnostics and driving behaviour intelligence")
    st.markdown("---")

    rng    = random.Random(HOUR * 3 + 7)
    em_pct = int(rng.random() * 75) + 20 if IS_RUSH else int(rng.random() * 45) + 10
    speed  = int(rng.random() * 30) + 15  if IS_RUSH else int(rng.random() * 50) + 50
    idle   = int(rng.random() * 8)
    rpm    = int(rng.random() * 3200) + 800

    if em_pct > 65:
        st.markdown('<div class="alert-red"><b style="color:#ef4444;font-size:1rem">🔴 HIGH EMISSION DETECTED</b><br><span style="color:#fca5a5;font-size:0.82rem">Above-normal emissions. Reduce speed and check diagnostics.</span></div>', unsafe_allow_html=True)
    elif em_pct > 40:
        st.markdown('<div class="alert-amber"><b style="color:#f59e0b;font-size:1rem">🟡 MODERATE EMISSIONS</b><br><span style="color:#fde68a;font-size:0.82rem">Slightly elevated — maintain steady speed and avoid sudden braking.</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-green"><b style="color:#22c55e;font-size:1rem">🟢 LOW EMISSIONS — CLEAN DRIVING</b><br><span style="color:#86efac;font-size:0.82rem">Excellent! Keep it up and earn Green Points.</span></div>', unsafe_allow_html=True)

    em_box  = "kpi-box-red"   if em_pct > 65 else ("kpi-box-amber" if em_pct > 40 else "")
    em_vc   = "kpi-val kpi-val-red" if em_pct > 65 else ("kpi-val kpi-val-amber" if em_pct > 40 else "kpi-val")
    idle_bc = "kpi-box-amber" if idle > 2 else ""
    idle_vc = "kpi-val kpi-val-amber" if idle > 2 else "kpi-val"
    rpm_bc  = "kpi-box-red"   if rpm > 3000 else ""
    rpm_vc  = "kpi-val kpi-val-red" if rpm > 3000 else "kpi-val"

    kpi_cols([
        (f"{em_pct}%",    "EMISSION LEVEL", em_box,          em_vc),
        (f"{speed} km/h", "SPEED",          "kpi-box-blue",  "kpi-val kpi-val-blue"),
        (f"{idle} min",   "IDLE TIME",      idle_bc,         idle_vc),
        (rpm,             "ENGINE RPM",     rpm_bc,          rpm_vc),
    ])

    st.markdown('<div class="sec-head">Speed &amp; Emission Relationship</div>', unsafe_allow_html=True)
    speeds     = [0,10,20,30,40,50,60,70,80,90,100,110,120]
    emissions  = [85,80,70,55,38,25,20,18,22,30,42,58,75]
    fig = go.Figure(go.Scatter(x=speeds, y=emissions, mode="lines",
                               line=dict(color="#22c55e", width=2)))
    fig.update_layout(**PLOTLY_LAYOUT, height=200,
                      xaxis_title="Speed (km/h)", yaxis_title="Emission %")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="alert-green"><b style="color:#22c55e">Key Insight</b> <span style="color:#86efac;font-size:0.82rem">Driving at a steady 60-80 km/h produces the least pollution. Stop-and-go and high speeds burn significantly more fuel.</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Action Plan</div>', unsafe_allow_html=True)
    actions = [
        ("🔧", "Check Engine Diagnostics",  "Run OBD scan or visit mechanic if emissions stay high.",         "#ef4444"),
        ("⛽", "Reduce Fuel Waste",          "Avoid rapid acceleration, maintain 60-80 km/h, reduce RPM.",     "#f59e0b"),
        ("🔩", "Service Your Vehicle",       "Oil change, air filter, fuel injector cleaning, exhaust check.", "#38bdf8"),
        ("🚫", "Stop Unnecessary Idling",    "Switch off engine after 1 minute of idling.",                    "#f59e0b"),
        ("🗺️","Switch to a Cleaner Route",  "Less traffic = less emissions. Open Smart Routes for options.",  "#22c55e"),
    ]
    for icon, title, desc, color in actions:
        st.markdown(f'<div class="action-card" style="border-left-color:{color}"><div style="color:{color};font-weight:700;font-size:0.88rem">{icon} {title}</div><div style="color:#94a3b8;font-size:0.82rem;margin-top:4px">{desc}</div></div>', unsafe_allow_html=True)

# ─── PAGE: ANALYTICS ─────────────────────────────────────────────────────────
def page_analytics():
    st.markdown("## 📊 Analytics")
    st.caption("Traffic and emission trends, zone status, cost impact")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Hourly Trends", "🗺️ Zone Emissions", "💰 Cost Impact", "🔥 Heatmap"])

    # ── TAB 1: Hourly Trends ──
    with tab1:
        st.markdown('<div class="sec-head">24-Hour Emission &amp; Speed Trends</div>', unsafe_allow_html=True)
        hours      = list(range(24))
        hourly_em  = []
        hourly_spd = []
        for h in hours:
            r  = random.Random(h * 5 + 3).random()
            em = int(r * 35) + 15
            if (7 <= h <= 9) or (16 <= h <= 18):
                em = min(100, em + 35)
            hourly_em.append(em)
            hourly_spd.append(max(10, 85 - em / 2))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[f"{h}:00" for h in hours], y=hourly_em,
                                 mode="lines", name="Emission %",
                                 line=dict(color="#ef4444", width=2)))
        fig.add_trace(go.Scatter(x=[f"{h}:00" for h in hours], y=hourly_spd,
                                 mode="lines", name="Speed km/h",
                                 line=dict(color="#38bdf8", width=2)))
        fig.update_layout(**PLOTLY_LAYOUT, height=250, legend=dict(font=dict(color="#94a3b8")))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="alert-amber"><b style="color:#f59e0b">Peak:</b> <span style="color:#fde68a;font-size:0.82rem">Rush hours 07:00–09:00 and 16:00–18:00. Cleanest window: 10:00–15:00.</span></div>', unsafe_allow_html=True)

    # ── TAB 2: Zone Emissions ──
    with tab2:
        st.markdown('<div class="sec-head">Zone Emission Status</div>', unsafe_allow_html=True)
        for i, name in enumerate(LOC_NAMES):
            c   = congestion_for(i * 11 + 2, HOUR)
            lvl = emission_level(c)
            col = lvl["color"]
            lbl = lvl["label"]
            pct = c
            st.markdown(f"""
<div style="background:#0a0f1e;border:1px solid #1e293b;border-radius:10px;padding:12px;margin-bottom:8px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
    <span style="font-weight:700;font-size:0.9rem">{name}</span>
    <span style="background:{col}22;color:{col};border:1px solid {col}55;border-radius:20px;padding:2px 10px;font-size:0.7rem;font-weight:700">{lbl}</span>
  </div>
  <div class="pbar-bg"><div class="pbar-fill" style="width:{pct}%;background:{col}"></div></div>
  <div style="color:#475569;font-size:0.78rem;margin-top:3px">{pct}% congestion</div>
</div>""", unsafe_allow_html=True)

    # ── TAB 3: Cost Impact ──
    with tab3:
        st.markdown('<div class="sec-head">Fuel Cost Impact Estimator</div>', unsafe_allow_html=True)
        weekly_km   = st.slider("Weekly Driving (km)", 50, 500, 200, key="an_km")
        fuel_price  = st.slider("Fuel Price (R/L)", 18, 30, 22, key="an_fuel")
        drive_style = st.selectbox("Driving Style", ["Aggressive", "Moderate", "Eco"], index=1, key="an_style")

        consumption = {"Aggressive": 12, "Moderate": 8, "Eco": 6}
        litres   = weekly_km / 100 * consumption[drive_style]
        cost_wk  = round(litres * fuel_price, 2)
        co2_wk   = round(litres * 2.31, 2)
        eco_save = round(max(0, (litres - weekly_km / 100 * 6) * fuel_price), 2)

        kpi_cols([
            (f"R{cost_wk}",                          "WEEKLY FUEL COST",  "kpi-box-amber", "kpi-val kpi-val-amber"),
            (f"{co2_wk} kg",                         "CO2 PER WEEK",      "kpi-box-red",   "kpi-val kpi-val-red"),
            (f"R{round(cost_wk * 4.3)}",             "MONTHLY COST",      "kpi-box-red",   "kpi-val kpi-val-red"),
            (f"R{eco_save}",                         "POTENTIAL SAVING/WK","",              "kpi-val"),
        ])

        if eco_save > 0:
            st.markdown(f'<div class="alert-amber" style="margin-top:10px"><b style="color:#f59e0b">Tip:</b> <span style="color:#fde68a;font-size:0.82rem">Switch to Eco driving to save R{eco_save}/week (R{round(eco_save*52)}/year).</span></div>', unsafe_allow_html=True)

    # ── TAB 4: Heatmap ──
    with tab4:
        st.markdown('<div class="sec-head">Weekly Emission Heatmap</div>', unsafe_allow_html=True)
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        hrs  = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

        z_vals = []
        for di, d in enumerate(days):
            row = []
            for h in hrs:
                r = random.Random(di * 100 + h).random()
                v = int(r * 70) + 10
                if h in [7, 8, 17, 18] and di < 5:
                    v = min(100, v + 35)
                row.append(v)
            z_vals.append(row)

        fig = go.Figure(go.Heatmap(
            z=z_vals,
            x=[f"{h}:00" for h in hrs],
            y=days,
            colorscale=[[0, "#14532d"], [0.4, "#78350f"], [1, "#7f1d1d"]],
            showscale=True,
            text=[[str(v) for v in row] for row in z_vals],
            texttemplate="%{text}",
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("🔴 Red = heavy congestion  ·  🟢 Green = smooth flow")

# ─── PAGE: ECO SCORE ─────────────────────────────────────────────────────────
def page_eco_score():
    st.markdown("## ⭐ Eco Score")
    st.caption("Your environmental driving rating")
    st.markdown("---")

    s     = st.session_state.eco_score
    grade = "A" if s >= 80 else ("B" if s >= 65 else ("C" if s >= 50 else "D"))
    g_col = "#22c55e" if s >= 80 else ("#4ade80" if s >= 65 else ("#f59e0b" if s >= 50 else "#ef4444"))
    label = ("Excellent Eco Driver" if s >= 80 else
             "Good Eco Driver"      if s >= 65 else
             "Average Driver"       if s >= 50 else "High Emission Driver")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
<div class="kpi-box" style="text-align:center;padding:24px">
  <div style="font-family:'Share Tech Mono',monospace;font-size:3.5rem;font-weight:900;color:{g_col}">{grade}</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:1.8rem;font-weight:900;color:{g_col}">{s}/100</div>
  <div style="color:#475569;font-size:0.6rem;letter-spacing:2px;margin-top:6px">{label.upper()}</div>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-head">Weekly Performance</div>', unsafe_allow_html=True)
        week_labels = ["6wk ago","5wk ago","4wk ago","3wk ago","2wk ago","Last wk","This wk"]
        scores      = st.session_state.weekly_scores
        fig = go.Figure(go.Scatter(x=week_labels, y=scores, mode="lines+markers",
                                   line=dict(color="#22c55e", width=2),
                                   marker=dict(color="#22c55e", size=6)))
        fig.update_layout(**PLOTLY_LAYOUT, height=180, yaxis_range=[40, 100])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="sec-head">Score Breakdown</div>', unsafe_allow_html=True)
    factors = [
        ("Route Choices",    78, "#22c55e"),
        ("Speed Consistency",65, "#4ade80"),
        ("Idle Management",  82, "#22c55e"),
        ("Trip Efficiency",  70, "#f59e0b"),
        ("Emission Level",   55, "#f59e0b"),
        ("Carpooling Bonus", 40, "#ef4444"),
    ]
    for name, val, col in factors:
        st.markdown(f"""
<div style="margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;margin-bottom:3px">
    <span style="font-size:0.85rem">{name}</span>
    <span style="color:{col};font-weight:700">{val}/100</span>
  </div>
  <div class="pbar-bg"><div class="pbar-fill" style="width:{val}%;background:{col}"></div></div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Driver Leaderboard</div>', unsafe_allow_html=True)
    username = st.session_state.username
    leaderboard = [
        {"Rank":"🥇 1st","Driver":"EcoDriver_01",           "Eco Score":96,"Green Pts":1240,"CO2 Saved":"148 kg"},
        {"Rank":"🥈 2nd","Driver":"GreenWheels",             "Eco Score":91,"Green Pts":985, "CO2 Saved":"118 kg"},
        {"Rank":"🥉 3rd","Driver":"CleanCommuter",           "Eco Score":88,"Green Pts":872, "CO2 Saved":"104 kg"},
        {"Rank":"4th",   "Driver":username,                  "Eco Score":s, "Green Pts":st.session_state.green_points,"CO2 Saved":f"{round(st.session_state.green_points*0.12,1)} kg"},
        {"Rank":"5th",   "Driver":"QuickRacer",              "Eco Score":43,"Green Pts":120, "CO2 Saved":"14 kg"},
    ]
    df = pd.DataFrame(leaderboard)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ─── PAGE: REWARDS ────────────────────────────────────────────────────────────
def page_rewards():
    st.markdown("## 🎁 Rewards")
    st.caption("Convert your Green Points into real-world rewards")
    st.markdown("---")

    pts = st.session_state.green_points
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f2a0a,#1a3a10);border:1px solid #166534;border-radius:14px;padding:24px;margin-bottom:16px">
  <div style="font-family:monospace;font-size:0.65rem;color:#86efac;letter-spacing:3px">MELLOWTECH REWARDS CARD</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:2.2rem;font-weight:900;color:#4ade80;margin:6px 0">{pts} pts</div>
  <div style="color:#22c55e;font-size:0.82rem">{st.session_state.username}</div>
  <div style="color:#475569;font-size:0.7rem;margin-top:4px">{DATE_STR} · ACTIVE</div>
</div>""", unsafe_allow_html=True)

    rewards = [
        ("⛽ Fuel Voucher",         50,  "Save R10 at participating fuel stations",  "#f59e0b"),
        ("💳 Petrol Discount 10%",  120, "10% off your next full tank",              "#f59e0b"),
        ("🛍️ Shopping Voucher R50", 100, "Redeem at partner retailers",              "#38bdf8"),
        ("🚌 Transport Credit",     80,  "Bus or taxi credit for 5 trips",           "#22c55e"),
        ("🔧 Free Vehicle Check",   200, "Emission diagnostic + engine check",       "#a78bfa"),
        ("🌳 Tree Planting Credit", 30,  "Sponsor a tree planted in your name",      "#22c55e"),
        ("🏪 Partner Discounts",    60,  "Discounts at eco-friendly stores",         "#38bdf8"),
        ("👑 Premium Eco Status",   500, "Unlock premium leaderboard + extra pts",   "#f59e0b"),
    ]

    cols = st.columns(2)
    for idx, (name, cost, desc, color) in enumerate(rewards):
        can    = pts >= cost
        border = color + "55" if can else "#1e293b"
        txt_c  = "#e2e8f0" if can else "#334155"
        status = "Tap to Redeem ✅" if can else f"Need {cost - pts} more"
        stat_c = color if can else "#334155"
        with cols[idx % 2]:
            st.markdown(f"""
<div class="reward-card" style="border-color:{border}">
  <div style="font-weight:700;font-size:0.88rem;color:{txt_c}">{name}</div>
  <div style="color:#475569;font-size:0.78rem;margin:4px 0">{desc}</div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
    <span style="font-family:monospace;font-size:1.1rem;font-weight:900;color:{color}">{cost} pts</span>
    <span style="font-size:0.7rem;font-weight:600;color:{stat_c}">{status}</span>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">How to Earn Green Points</div>', unsafe_allow_html=True)
    earn_tips = [
        ("🗺️ Clean Routes",     "+15 pts/trip"),
        ("⚡ Steady Speed",      "+5 pts/trip"),
        ("🚌 Public Transport",  "+20 pts/trip"),
        ("🚫 No Idling",         "+3 pts"),
        ("🤝 Carpool",           "+25 pts/trip"),
        ("🔧 Vehicle Service",   "+50 pts"),
    ]
    cols2 = st.columns(2)
    for idx, (tip, val) in enumerate(earn_tips):
        with cols2[idx % 2]:
            st.markdown(f"""
<div style="background:#071a0e;border:1px solid #14532d;border-radius:10px;padding:12px;text-align:center;margin-bottom:8px">
  <div style="font-weight:700;font-size:0.85rem;color:#4ade80">{tip}</div>
  <div style="font-family:monospace;color:#22c55e;font-size:0.95rem;font-weight:900;margin-top:4px">{val}</div>
</div>""", unsafe_allow_html=True)

# ─── PAGE: PROFILE ────────────────────────────────────────────────────────────
def page_profile():
    st.markdown("## 👤 Profile")
    st.caption("Your account and preferences")
    st.markdown("---")

    s     = st.session_state.eco_score
    grade = "A" if s >= 80 else ("B" if s >= 65 else ("C" if s >= 50 else "D"))
    g_col = "#22c55e" if s >= 80 else ("#4ade80" if s >= 65 else ("#f59e0b" if s >= 50 else "#ef4444"))
    co2   = round(st.session_state.green_points * 0.12, 2)
    fuel  = round(st.session_state.green_points * 0.05, 2)
    money = round(fuel * 22, 2)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
<div class="kpi-box" style="text-align:center;padding:24px">
  <div style="font-size:2.5rem">🌿</div>
  <div style="font-size:1.05rem;font-weight:900;color:#22c55e;margin-top:8px">{st.session_state.username}</div>
  <span class="badge" style="margin-top:6px;display:inline-block">GRADE {grade}</span>
  <hr style="border-color:#1e293b;margin:12px 0">
  <div style="color:#475569;font-size:0.7rem">Member since {now.strftime("%b %Y")}</div>
  <div style="font-family:monospace;font-size:1.7rem;font-weight:900;color:{g_col};margin-top:10px">{s}/100</div>
  <div style="color:#475569;font-size:0.6rem;letter-spacing:2px">ECO SCORE</div>
  <div style="font-family:monospace;font-size:1.4rem;font-weight:900;color:#4ade80;margin-top:8px">{st.session_state.green_points}</div>
  <div style="color:#475569;font-size:0.6rem;letter-spacing:2px">GREEN POINTS</div>
</div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("**Preferences**")
        new_name  = st.text_input("Display Name",          value=st.session_state.username,     key="prof_name")
        new_home  = st.selectbox("Home Location",          LOC_NAMES,
                                  index=LOC_NAMES.index(st.session_state.home_loc), key="prof_home")
        new_mode  = st.selectbox("Default Driving Mode",   ["Eco Mode","Normal Mode","Fast Mode"],
                                  index=["Eco Mode","Normal Mode","Fast Mode"].index(st.session_state.driving_mode), key="prof_mode")
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.username     = new_name
            st.session_state.home_loc     = new_home
            st.session_state.driving_mode = new_mode
            st.success("✅ Preferences saved!")
            st.rerun()

    st.markdown('<div class="sec-head">My Environmental Impact</div>', unsafe_allow_html=True)
    kpi_cols([
        (f"{co2} kg",  "CO2 SAVED",   "",             "kpi-val"),
        (f"{fuel} L",  "FUEL SAVED",  "kpi-box-amber","kpi-val kpi-val-amber"),
        (f"R{money}",  "MONEY SAVED", "kpi-box-blue", "kpi-val kpi-val-blue"),
        (st.session_state.trips,"TRIPS DONE","",       "kpi-val"),
    ])

    st.markdown('<div class="alert-green" style="margin-top:12px"><b style="color:#22c55e">Your Climate Contribution</b><br><span style="color:#86efac;font-size:0.82rem">By using MellowTech you help reduce urban air pollution and contribute to South Africa\'s climate goals. Every clean trip counts.</span></div>', unsafe_allow_html=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        show_login()
        return

    show_sidebar()

    page = st.session_state.page
    if   page == "Dashboard":       page_dashboard()
    elif page == "Smart Routes":    page_smart_routes()
    elif page == "Emission Alerts": page_emission_alerts()
    elif page == "Analytics":       page_analytics()
    elif page == "Eco Score":       page_eco_score()
    elif page == "Rewards":         page_rewards()
    elif page == "Profile":         page_profile()
    else:
        page_dashboard()

if __name__ == "__main__":
    main()
