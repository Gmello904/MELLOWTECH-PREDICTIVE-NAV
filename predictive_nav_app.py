import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }

.mt-title  { font-family: 'Share Tech Mono', monospace; font-size: 2.2rem; font-weight: 900;
             color: #4ade80; letter-spacing: 4px; text-align: center; }
.mt-sub    { color: #475569; font-size: 11px; letter-spacing: 6px; text-transform: uppercase;
             text-align: center; margin-bottom: 1.5rem; }
.page-head { color: #e2e8f0; font-size: 1.4rem; font-weight: 900; margin-bottom: 0; }
.page-sub  { color: #475569; font-size: 12px; margin-top: 0; }

.kpi-card  { background: linear-gradient(135deg, #0a0f1e, #0f1929);
             border: 1px solid #1e293b; border-radius: 14px; padding: 18px 14px;
             text-align: center; position: relative; overflow: hidden; }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px;
                    background: linear-gradient(90deg,transparent,#22c55e,transparent); }
.kpi-card.red::before   { background: linear-gradient(90deg,transparent,#ef4444,transparent); }
.kpi-card.amber::before { background: linear-gradient(90deg,transparent,#f59e0b,transparent); }
.kpi-card.blue::before  { background: linear-gradient(90deg,transparent,#38bdf8,transparent); }

.kpi-val        { font-family: 'Share Tech Mono', monospace; font-size: 1.7rem; font-weight: 900; color: #4ade80; }
.kpi-val.red    { color: #ef4444; }
.kpi-val.amber  { color: #f59e0b; }
.kpi-val.blue   { color: #38bdf8; }
.kpi-lbl        { font-size: 9px; letter-spacing: 3px; color: #475569; text-transform: uppercase; margin-top: 4px; }

.alert-red   { background: #1c0a0a; border: 1px solid #7f1d1d; border-left: 4px solid #ef4444;
               border-radius: 10px; padding: 12px 16px; margin: 8px 0; }
.alert-green { background: #071a0e; border: 1px solid #14532d; border-left: 4px solid #22c55e;
               border-radius: 10px; padding: 12px 16px; margin: 8px 0; }
.alert-amber { background: #1a1203; border: 1px solid #78350f; border-left: 4px solid #f59e0b;
               border-radius: 10px; padding: 12px 16px; margin: 8px 0; }

.pbar-bg   { background: #1e293b; border-radius: 20px; height: 8px; margin: 6px 0; }
.pbar-fill { height: 8px; border-radius: 20px; }

.badge { display:inline-block; background:#0d2318; color:#4ade80; border:1px solid #166534;
         border-radius:20px; padding:3px 12px; font-size:11px; letter-spacing:2px; }

.action-card { background:#0a0f1e; border:1px solid #1e293b; border-radius:10px;
               padding:14px; margin-bottom:8px; }
.reward-card { background:#0a0f1e; border:1px solid #1e293b; border-radius:12px;
               padding:14px; margin-bottom:10px; }
.route-blue  { background:#071520; border:2px solid #38bdf8; border-radius:14px; padding:16px; }
.route-red   { background:#1c0a0a; border:2px solid #ef4444; border-radius:14px; padding:16px; }
.mono-val    { font-family:'Share Tech Mono',monospace; font-size:1.3rem; font-weight:900; }
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
    s = [int(seed) & 0xFFFFFFFF]
    def _next():
        s[0] = (s[0] * 1664525 + 1013904223) & 0xFFFFFFFF
        return s[0] / 0xFFFFFFFF
    return _next

def congestion_for(seed, hr):
    r = seeded_rand(seed)
    v = int(r() * 55) + 15
    if (7 <= hr <= 9) or (16 <= hr <= 18):
        v = min(100, v + 30)
    return v

def emission_level(c):
    if c > 65:
        return {"label": "HIGH",   "color": "#ef4444"}
    if c > 40:
        return {"label": "MEDIUM", "color": "#f59e0b"}
    return {"label": "LOW",        "color": "#22c55e"}

now      = datetime.now()
HOUR     = now.hour
IS_RUSH  = (7 <= HOUR <= 9) or (16 <= HOUR <= 18)
TIME_STR = now.strftime("%H:%M")
DATE_STR = now.strftime("%d %b %Y")

# ─── SESSION STATE INIT ──────────────────────────────────────────────────────
def init_state():
    defaults = {
        "logged_in":     False,
        "page":          "dashboard",
        "username":      "",
        "green_points":  0,
        "eco_score":     72,
        "trips":         0,
        "home_loc":      "Home",
        "driving_mode":  "Normal Mode",
        "weekly_scores": [55, 61, 58, 67, 70, 68, 72],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── HTML HELPERS ─────────────────────────────────────────────────────────────
def kpi_card(value, label, color_cls=""):
    return f"""
    <div class="kpi-card {color_cls}">
      <div class="kpi-val {color_cls}">{value}</div>
      <div class="kpi-lbl">{label}</div>
    </div>"""

def progress_bar(pct, color):
    return f"""
    <div class="pbar-bg">
      <div class="pbar-fill" style="width:{pct}%;background:{color};"></div>
    </div>"""

# ─── LOGIN PAGE ──────────────────────────────────────────────────────────────
def login_page():
    st.markdown('<div class="mt-title">🌿 MELLOWTECH</div>', unsafe_allow_html=True)
    st.markdown('<div class="mt-sub">Smart Emission Intelligence System</div>', unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### 🔑 Sign In")
        st.caption("PROTECTING THE PLANET, ONE TRIP AT A TIME")
        uname = st.text_input("Username", placeholder="Enter username", key="login_uname")
        pwd   = st.text_input("Password", placeholder="Enter password", type="password", key="login_pwd")
        if st.button("🚀 Launch MellowTech", use_container_width=True, type="primary"):
            if not uname.strip():
                st.error("Please enter a username.")
            elif not pwd:
                st.error("Please enter a password.")
            else:
                st.session_state["logged_in"] = True
                st.session_state["username"]  = uname.strip()
                st.rerun()
        st.caption("Demo: any username + any password")

# ─── SIDEBAR NAV ─────────────────────────────────────────────────────────────
def sidebar_nav():
    with st.sidebar:
        st.markdown("### 🌿 MELLOWTECH")
        st.caption("EMISSION INTELLIGENCE")
        st.divider()
        st.markdown(f"**👤 {st.session_state['username']}**")
        st.markdown(f"🟢 {st.session_state['green_points']} Green Points")
        st.divider()

        nav_items = [
            ("dashboard", "🏠 Dashboard"),
            ("routes",    "🗺️ Smart Routes"),
            ("alerts",    "⚠️ Emission Alerts"),
            ("analytics", "📊 Analytics"),
            ("ecoscore",  "⭐ Eco Score"),
            ("rewards",   "🎁 Rewards"),
            ("profile",   "👤 Profile"),
        ]
        for page_id, label in nav_items:
            active = st.session_state["page"] == page_id
            if st.button(label, key=f"nav_{page_id}",
                         use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state["page"] = page_id
                st.rerun()

        st.divider()
        eco = st.session_state["eco_score"]
        st.caption("ECO SCORE")
        st.progress(eco / 100)
        st.markdown(f"**{eco}/100**")
        st.divider()
        if st.button("🔓 Sign Out", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            init_state()
            st.rerun()

# ─── PAGE: DASHBOARD ─────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown('<p class="page-head">🏠 Dashboard</p>', unsafe_allow_html=True)
    st.caption("Live emission intelligence overview")
    st.divider()

    gp      = st.session_state["green_points"]
    eco     = st.session_state["eco_score"]
    trips   = st.session_state["trips"]
    savings = round(gp * 0.12, 2)
    fuel    = round(gp * 0.05, 2)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(TIME_STR, DATE_STR, "blue"), unsafe_allow_html=True)
    with c2:
        label = "RUSH HOUR" if IS_RUSH else "CLEAR"
        cls   = "red" if IS_RUSH else ""
        st.markdown(kpi_card(label, "TRAFFIC STATUS", cls), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(f"{eco}/100", "ECO SCORE"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(gp, "GREEN POINTS"), unsafe_allow_html=True)

    st.markdown("")
    if IS_RUSH:
        st.markdown('<div class="alert-red"><b style="color:#ef4444">⚠️ HIGH EMISSION ALERT</b><br>'
                    '<span style="color:#fca5a5;font-size:13px">Rush hour — consider delaying or choosing a clean route.</span></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-green"><b style="color:#22c55e">✅ LOW EMISSION CONDITIONS</b><br>'
                    '<span style="color:#86efac;font-size:13px">Traffic is clear — great time to travel and earn Green Points.</span></div>',
                    unsafe_allow_html=True)

    st.markdown("**Real-Time City Emission Pulse**")
    pulse_data = [{"name": n, "value": congestion_for(i * 7 + 1, HOUR)} for i, n in enumerate(LOC_NAMES)]
    df_pulse = pd.DataFrame(pulse_data)
    df_pulse["color"] = df_pulse["value"].apply(lambda v: emission_level(v)["color"])

    fig = go.Figure(go.Bar(
        x=df_pulse["name"], y=df_pulse["value"],
        marker_color=df_pulse["color"].tolist(),
        marker_line_width=0,
    ))
    fig.update_layout(
        plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e",
        font_color="#475569", height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b", range=[0, 100]),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Today's Impact**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(f"{savings} kg", "CO2 SAVED TODAY"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(f"R{fuel}", "FUEL COST SAVED", "amber"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(trips, "TRIPS COMPLETED", "blue"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(gp, "TOTAL GREEN POINTS"), unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="alert-green"><b style="color:#22c55e">Why It Matters</b><br>'
                '<span style="color:#86efac;font-size:13px">Every clean trip earns Green Points redeemable for real rewards while reducing urban air pollution.</span></div>',
                unsafe_allow_html=True)

# ─── PAGE: SMART ROUTES ──────────────────────────────────────────────────────
def page_routes():
    st.markdown('<p class="page-head">🗺️ Smart Routes</p>', unsafe_allow_html=True)
    st.caption("Choose cleaner routes — reduce emissions, earn Green Points")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        origin = st.selectbox("ORIGIN", LOC_NAMES, key="route_origin")
    with c2:
        dest_opts = [l for l in LOC_NAMES if l != origin]
        dest = st.selectbox("DESTINATION", dest_opts, key="route_dest")

    leave_hr = st.slider("DEPARTURE HOUR", 0, 23, HOUR, format="%d:00", key="route_hour")

    seed_val = leave_hr + ord(origin[0]) + ord(dest[0])
    r = seeded_rand(seed_val)
    cong_a = min(100, int(r() * 35) + 10)
    cong_b = min(100, int(r() * 40) + 50 + (25 if IS_RUSH else 0))
    dist_a = round(r() * 14 + 4, 1)
    dist_b = round(dist_a * (r() * 0.5 + 0.8), 1)
    time_a = round(dist_a * 1.5 + cong_a * 0.3)
    time_b = round(dist_b * 1.5 + cong_b * 0.5)
    fuel_a = round(dist_a * 0.08, 2)
    fuel_b = round(dist_b * 0.08 + cong_b * 0.005, 2)
    co2_a  = round(fuel_a * 2.31, 2)
    co2_b  = round(fuel_b * 2.31, 2)

    st.markdown("")
    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown(f"""
        <div class="route-blue">
          <div style="font-size:14px;font-weight:800;color:#38bdf8">✅ CLEAN ROUTE</div>
          <div style="color:#7dd3fc;font-size:10px;letter-spacing:2px;margin-bottom:10px">LOW EMISSIONS · RECOMMENDED</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div><div class="mono-val" style="color:#38bdf8">{cong_a}%</div><div style="color:#64748b;font-size:10px">CONGESTION</div></div>
            <div><div class="mono-val" style="color:#38bdf8">{time_a} min</div><div style="color:#64748b;font-size:10px">TIME</div></div>
            <div><div class="mono-val" style="color:#4ade80">{dist_a} km</div><div style="color:#64748b;font-size:10px">DISTANCE</div></div>
            <div><div class="mono-val" style="color:#4ade80">{co2_a} kg</div><div style="color:#64748b;font-size:10px">CO2</div></div>
          </div>
          <div style="margin-top:10px;background:#0a1a2e;border-radius:8px;padding:8px;font-size:12px;color:#7dd3fc">
            Smooth flow · Earn +15 Green Points
          </div>
        </div>""", unsafe_allow_html=True)
    with rc2:
        st.markdown(f"""
        <div class="route-red">
          <div style="font-size:14px;font-weight:800;color:#ef4444">⛔ HIGH EMISSION ROUTE</div>
          <div style="color:#fca5a5;font-size:10px;letter-spacing:2px;margin-bottom:10px">HEAVY TRAFFIC · AVOID</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div><div class="mono-val" style="color:#ef4444">{cong_b}%</div><div style="color:#64748b;font-size:10px">CONGESTION</div></div>
            <div><div class="mono-val" style="color:#ef4444">{time_b} min</div><div style="color:#64748b;font-size:10px">TIME</div></div>
            <div><div class="mono-val" style="color:#f87171">{dist_b} km</div><div style="color:#64748b;font-size:10px">DISTANCE</div></div>
            <div><div class="mono-val" style="color:#f87171">{co2_b} kg</div><div style="color:#64748b;font-size:10px">CO2</div></div>
          </div>
          <div style="margin-top:10px;background:#1c0808;border-radius:8px;padding:8px;font-size:12px;color:#fca5a5">
            Stop-and-go · High idling · More fuel
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    co2_diff  = round(co2_b - co2_a, 2)
    fuel_diff = round((fuel_b - fuel_a) * 20, 2)
    st.markdown(f'<div class="alert-green"><b style="color:#22c55e">Smart Advisor</b><br>'
                f'<span style="color:#86efac;font-size:13px">Taking the Clean Route saves <b>{co2_diff} kg CO2</b> '
                f'and ~<b>R{fuel_diff}</b> in fuel. Earn <b>+15 Green Points</b>.</span></div>',
                unsafe_allow_html=True)

    if st.button("🚗 Take Clean Route — Start Trip", type="primary", use_container_width=True):
        st.session_state["green_points"] += 15
        st.session_state["trips"]        += 1
        st.session_state["eco_score"]     = min(100, st.session_state["eco_score"] + 1)
        st.success(f"✅ Trip started! +15 pts added. Total: {st.session_state['green_points']} pts")
        st.rerun()

# ─── PAGE: EMISSION ALERTS ───────────────────────────────────────────────────
def page_alerts():
    st.markdown('<p class="page-head">⚠️ Emission Alerts</p>', unsafe_allow_html=True)
    st.caption("Live diagnostics and driving behaviour intelligence")
    st.divider()

    r      = seeded_rand(HOUR * 3 + 7)
    em_pct = int(r() * 75) + 20 if IS_RUSH else int(r() * 45) + 10
    speed  = int(r() * 30) + 15 if IS_RUSH else int(r() * 50) + 50
    idle   = int(r() * 8)
    rpm    = int(r() * 3200) + 800

    if em_pct > 65:
        st.markdown('<div class="alert-red"><b style="color:#ef4444;font-size:16px">🔴 HIGH EMISSION DETECTED</b><br>'
                    '<span style="color:#fca5a5;font-size:13px">Above-normal emissions. Reduce speed and check diagnostics.</span></div>',
                    unsafe_allow_html=True)
    elif em_pct > 40:
        st.markdown('<div class="alert-amber"><b style="color:#f59e0b;font-size:16px">🟡 MODERATE EMISSIONS</b><br>'
                    '<span style="color:#fde68a;font-size:13px">Slightly elevated — maintain steady speed and avoid sudden braking.</span></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-green"><b style="color:#22c55e;font-size:16px">🟢 LOW EMISSIONS — CLEAN DRIVING</b><br>'
                    '<span style="color:#86efac;font-size:13px">Excellent! Keep it up and earn Green Points.</span></div>',
                    unsafe_allow_html=True)

    em_cls  = "red"   if em_pct > 65 else ("amber" if em_pct > 40 else "")
    id_cls  = "amber" if idle > 2     else ""
    rpm_cls = "red"   if rpm > 3000   else ""

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(f"{em_pct}%",   "EMISSION LEVEL", em_cls),  unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(f"{speed} km/h", "SPEED",          "blue"),  unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(f"{idle} min",   "IDLE TIME",       id_cls), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(rpm,             "ENGINE RPM",      rpm_cls),unsafe_allow_html=True)

    st.markdown("")
    st.markdown("**Speed & Emission Relationship**")
    speed_vals = [0,10,20,30,40,50,60,70,80,90,100,110,120]
    em_vals    = [85,80,70,55,38,25,20,18,22,30,42,58,75]
    fig = go.Figure(go.Scatter(
        x=speed_vals, y=em_vals, mode="lines",
        line=dict(color="#22c55e", width=2),
    ))
    fig.update_layout(
        plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e",
        font_color="#475569", height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Speed (km/h)", gridcolor="#1e293b"),
        yaxis=dict(title="Emission %",   gridcolor="#1e293b"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="alert-green"><b style="color:#22c55e">Key Insight</b> '
                '<span style="color:#86efac;font-size:13px">Driving at a steady 60-80 km/h produces the least pollution. '
                'Stop-and-go and high speeds burn significantly more fuel.</span></div>',
                unsafe_allow_html=True)

    st.markdown("**Action Plan**")
    actions = [
        ("🔧", "Check Engine Diagnostics",  "Run OBD scan or visit mechanic if emissions stay high.",         "#ef4444"),
        ("⛽", "Reduce Fuel Waste",          "Avoid rapid acceleration, maintain 60-80 km/h, reduce RPM.",     "#f59e0b"),
        ("🔩", "Service Your Vehicle",       "Oil change, air filter, fuel injector cleaning, exhaust check.", "#38bdf8"),
        ("🚫", "Stop Unnecessary Idling",    "Switch off engine after 1 minute of idling.",                    "#f59e0b"),
        ("🗺️", "Switch to a Cleaner Route", "Less traffic = less emissions. Open Smart Routes for options.",  "#22c55e"),
    ]
    for icon, title, desc, color in actions:
        st.markdown(f"""
        <div class="action-card" style="border-left:3px solid {color}">
          <div style="color:{color};font-weight:700;font-size:14px">{icon} {title}</div>
          <div style="color:#94a3b8;font-size:13px;margin-top:4px">{desc}</div>
        </div>""", unsafe_allow_html=True)

# ─── PAGE: ANALYTICS ─────────────────────────────────────────────────────────
def page_analytics():
    st.markdown('<p class="page-head">📊 Analytics</p>', unsafe_allow_html=True)
    st.caption("Traffic and emission trends, zone status, cost impact")
    st.divider()

    tab0, tab1, tab2, tab3 = st.tabs(["📈 Hourly Trends", "🗺️ Zone Emissions", "💰 Cost Impact", "🔥 Heatmap"])

    with tab0:
        st.markdown("**24-Hour Emission & Speed Trends**")
        hourly = []
        for h in range(24):
            r  = seeded_rand(h * 5 + 3)
            em = int(r() * 35) + 15
            if (7 <= h <= 9) or (16 <= h <= 18):
                em = min(100, em + 35)
            hourly.append({"hour": f"{h}:00", "emission": em, "speed": max(10, 85 - em // 2)})
        df_h = pd.DataFrame(hourly)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_h["hour"], y=df_h["emission"], name="Emission %",
                                 line=dict(color="#ef4444", width=2), mode="lines"))
        fig.add_trace(go.Scatter(x=df_h["hour"], y=df_h["speed"],    name="Speed km/h",
                                 line=dict(color="#38bdf8", width=2), mode="lines"))
        fig.update_layout(
            plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e", font_color="#475569",
            height=240, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#1e293b", tickangle=-45),
            yaxis=dict(gridcolor="#1e293b"),
            legend=dict(bgcolor="#0a0f1e", bordercolor="#1e293b"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="alert-amber"><b style="color:#f59e0b">Peak:</b> '
                    '<span style="color:#fde68a;font-size:13px">Rush hours 07:00–09:00 and 16:00–18:00. '
                    'Cleanest window: 10:00–15:00.</span></div>', unsafe_allow_html=True)

    with tab1:
        st.markdown("**Zone Emission Status**")
        for i, name in enumerate(LOC_NAMES):
            c  = congestion_for(i * 11 + 2, HOUR)
            el = emission_level(c)
            st.markdown(f"""
            <div style="background:#0a0f1e;border:1px solid #1e293b;border-radius:10px;padding:12px;margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span style="font-weight:700;font-size:14px;color:#e2e8f0">{name}</span>
                <span style="background:{el['color']}22;color:{el['color']};border:1px solid {el['color']}55;
                             border-radius:20px;padding:2px 10px;font-size:11px;font-weight:700">{el['label']}</span>
              </div>
              {progress_bar(c, el['color'])}
              <div style="color:#64748b;font-size:12px">{c}% congestion</div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("**Fuel Cost Impact Estimator**")
        weekly_km   = st.slider("Weekly Driving (km)", 50, 500, 200, key="ana_km")
        fuel_price  = st.slider("Fuel Price (R/L)",    18, 30,   22, key="ana_fp")
        drive_style = st.selectbox("Driving Style", ["Aggressive", "Moderate", "Eco"], index=1, key="ana_ds")
        cons_map    = {"Aggressive": 12, "Moderate": 8, "Eco": 6}
        litres   = weekly_km / 100 * cons_map[drive_style]
        cost_wk  = round(litres * fuel_price, 2)
        co2_wk   = round(litres * 2.31, 2)
        eco_save = max(0.0, round((litres - weekly_km / 100 * 6) * fuel_price, 2))

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(kpi_card(f"R{cost_wk}",              "WEEKLY FUEL COST",  "amber"), unsafe_allow_html=True)
        with c2:
            st.markdown(kpi_card(f"{co2_wk} kg",             "CO2 PER WEEK",      "red"),   unsafe_allow_html=True)
        with c3:
            st.markdown(kpi_card(f"R{round(cost_wk*4.3)}",   "MONTHLY COST",      "red"),   unsafe_allow_html=True)
        with c4:
            st.markdown(kpi_card(f"R{eco_save}",             "POTENTIAL SAVING/WK"),         unsafe_allow_html=True)

        if eco_save > 0:
            st.markdown(f'<div class="alert-amber" style="margin-top:10px"><b style="color:#f59e0b">Tip:</b> '
                        f'<span style="color:#fde68a;font-size:13px">Switch to Eco driving to save R{eco_save}/week '
                        f'(R{round(eco_save*52)}/year).</span></div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("**Weekly Emission Heatmap**")
        DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        HRS  = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        z_data = []
        for di, _ in enumerate(DAYS):
            row = []
            for h in HRS:
                r = seeded_rand(di * 100 + h)
                v = int(r() * 70) + 10
                if h in [7, 8, 17, 18] and di < 5:
                    v = min(100, v + 35)
                row.append(v)
            z_data.append(row)

        fig = go.Figure(go.Heatmap(
            z=z_data,
            x=[f"{h}:00" for h in HRS],
            y=DAYS,
            colorscale=[[0, "#14532d"], [0.4, "#166534"], [0.65, "#78350f"], [1, "#7f1d1d"]],
            text=[[str(v) for v in row] for row in z_data],
            texttemplate="%{text}",
            showscale=True,
            zmin=0, zmax=100,
        ))
        fig.update_layout(
            plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e", font_color="#94a3b8",
            height=280, margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔴 Red = heavy congestion · 🟢 Green = smooth flow")

# ─── PAGE: ECO SCORE ─────────────────────────────────────────────────────────
def page_ecoscore():
    st.markdown('<p class="page-head">⭐ Eco Score</p>', unsafe_allow_html=True)
    st.caption("Your environmental driving rating")
    st.divider()

    s     = st.session_state["eco_score"]
    gp    = st.session_state["green_points"]
    uname = st.session_state["username"]
    grade = "A" if s >= 80 else ("B" if s >= 65 else ("C" if s >= 50 else "D"))
    g_col = "#22c55e" if s >= 80 else ("#4ade80" if s >= 65 else ("#f59e0b" if s >= 50 else "#ef4444"))
    label = ("Excellent Eco Driver" if s >= 80 else
             "Good Eco Driver"      if s >= 65 else
             "Average Driver"       if s >= 50 else "High Emission Driver")

    weekly_scores = st.session_state["weekly_scores"]
    week_labels   = ["6wk ago","5wk ago","4wk ago","3wk ago","2wk ago","Last wk","This wk"]

    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="padding:28px 20px;text-align:center">
          <div style="font-family:'Share Tech Mono',monospace;font-size:3.5rem;font-weight:900;color:{g_col}">{grade}</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:1.8rem;font-weight:900;color:{g_col}">{s}/100</div>
          <div style="color:#64748b;font-size:10px;letter-spacing:2px;margin-top:8px">{label.upper()}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("**Weekly Performance**")
        fig = go.Figure(go.Scatter(
            x=week_labels, y=weekly_scores, mode="lines+markers",
            line=dict(color="#22c55e", width=2),
            marker=dict(color="#22c55e", size=6),
        ))
        fig.update_layout(
            plot_bgcolor="#0a0f1e", paper_bgcolor="#0a0f1e", font_color="#475569",
            height=180, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b", range=[40, 100]),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Score Breakdown**")
    factors = [
        ("Route Choices",     78, "#22c55e"),
        ("Speed Consistency", 65, "#4ade80"),
        ("Idle Management",   82, "#22c55e"),
        ("Trip Efficiency",   70, "#f59e0b"),
        ("Emission Level",    55, "#f59e0b"),
        ("Carpooling Bonus",  40, "#ef4444"),
    ]
    for fname, val, color in factors:
        st.markdown(f"""
        <div style="margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="font-size:13px;color:#e2e8f0">{fname}</span>
            <span style="color:{color};font-weight:700">{val}/100</span>
          </div>
          {progress_bar(val, color)}
        </div>""", unsafe_allow_html=True)

    st.markdown("**Driver Leaderboard**")
    leaderboard = [
        {"rank": "🥇 1st", "driver": "EcoDriver_01",  "score": 96, "pts": 1240, "co2": 148},
        {"rank": "🥈 2nd", "driver": "GreenWheels",    "score": 91, "pts": 985,  "co2": 118},
        {"rank": "🥉 3rd", "driver": "CleanCommuter",  "score": 88, "pts": 872,  "co2": 104},
        {"rank": "4th",    "driver": uname,             "score": s,  "pts": gp,   "co2": round(gp * 0.12, 1)},
        {"rank": "5th",    "driver": "QuickRacer",      "score": 43, "pts": 120,  "co2": 14},
    ]
    headers     = ["Rank", "Driver", "Eco Score", "Green Pts", "CO2 Saved"]
    header_html = "".join(f'<th style="padding:8px 10px;color:#475569;text-align:left;font-size:11px">{h}</th>'
                          for h in headers)
    rows_html = ""
    for row in leaderboard:
        is_me   = row["driver"] == uname
        bg      = "#0d2318"  if is_me else "transparent"
        dcol    = "#4ade80"  if is_me else "#e2e8f0"
        dweight = "700"      if is_me else "400"
        rows_html += (
            f'<tr style="border-bottom:1px solid #1e293b;background:{bg}">'
            f'<td style="padding:8px 10px;color:#e2e8f0">{row["rank"]}</td>'
            f'<td style="padding:8px 10px;color:{dcol};font-weight:{dweight}">{row["driver"]}</td>'
            f'<td style="padding:8px 10px;font-family:monospace;color:#4ade80">{row["score"]}</td>'
            f'<td style="padding:8px 10px;font-family:monospace;color:#f59e0b">{row["pts"]}</td>'
            f'<td style="padding:8px 10px;font-family:monospace;color:#38bdf8">{row["co2"]} kg</td>'
            f'</tr>'
        )
    st.markdown(f"""
    <div style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:13px">
        <thead><tr style="border-bottom:1px solid #1e293b">{header_html}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)

# ─── PAGE: REWARDS ───────────────────────────────────────────────────────────
def page_rewards():
    st.markdown('<p class="page-head">🎁 Rewards</p>', unsafe_allow_html=True)
    st.caption("Convert your Green Points into real-world rewards")
    st.divider()

    pts   = st.session_state["green_points"]
    uname = st.session_state["username"]

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f2a0a,#1a3a10);border:1px solid #166534;
                border-radius:16px;padding:24px;margin-bottom:16px">
      <div style="font-family:monospace;font-size:10px;color:#86efac;letter-spacing:3px">MELLOWTECH REWARDS CARD</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:2.2rem;font-weight:900;color:#4ade80;margin:6px 0">{pts} pts</div>
      <div style="color:#22c55e;font-size:13px">{uname}</div>
      <div style="color:#64748b;font-size:11px;margin-top:4px">{DATE_STR} · ACTIVE</div>
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
    for idx, (rname, cost, desc, color) in enumerate(rewards):
        can    = pts >= cost
        border = f"{color}55" if can else "#1e293b"
        ncol   = "#e2e8f0"    if can else "#334155"
        action = "✅ Tap to Redeem" if can else f"Need {cost - pts} more"
        acol   = color             if can else "#334155"
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="reward-card" style="border-color:{border}">
              <div style="font-weight:700;font-size:14px;color:{ncol}">{rname}</div>
              <div style="color:#64748b;font-size:12px;margin:4px 0">{desc}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
                <span style="font-family:monospace;font-size:1.1rem;font-weight:900;color:{color}">{cost} pts</span>
                <span style="font-size:11px;font-weight:600;color:{acol}">{action}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("**How to Earn Green Points**")
    earn_tips = [
        ("🗺️ Clean Routes",     "+15 pts/trip"),
        ("⚡ Steady Speed",      "+5 pts/trip"),
        ("🚌 Public Transport",  "+20 pts/trip"),
        ("🚫 No Idling",         "+3 pts"),
        ("🤝 Carpool",           "+25 pts/trip"),
        ("🔧 Vehicle Service",   "+50 pts"),
    ]
    tip_cols = st.columns(2)
    for i, (tip, val) in enumerate(earn_tips):
        with tip_cols[i % 2]:
            st.markdown(f"""
            <div style="background:#071a0e;border:1px solid #14532d;border-radius:10px;
                        padding:12px;text-align:center;margin-bottom:8px">
              <div style="font-weight:700;font-size:13px;color:#4ade80">{tip}</div>
              <div style="font-family:monospace;color:#22c55e;font-size:15px;font-weight:900;margin-top:4px">{val}</div>
            </div>""", unsafe_allow_html=True)

# ─── PAGE: PROFILE ────────────────────────────────────────────────────────────
def page_profile():
    st.markdown('<p class="page-head">👤 Profile</p>', unsafe_allow_html=True)
    st.caption("Your account and preferences")
    st.divider()

    s     = st.session_state["eco_score"]
    gp    = st.session_state["green_points"]
    trips = st.session_state["trips"]
    grade = "A" if s >= 80 else ("B" if s >= 65 else ("C" if s >= 50 else "D"))
    g_col = "#22c55e" if s >= 80 else ("#4ade80" if s >= 65 else ("#f59e0b" if s >= 50 else "#ef4444"))
    co2   = round(gp * 0.12, 2)
    fuel  = round(gp * 0.05, 2)
    join  = now.strftime("%b %Y")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="text-align:center;padding:28px 16px">
          <div style="font-size:44px">🌿</div>
          <div style="font-size:17px;font-weight:900;color:#22c55e;margin-top:8px">{st.session_state['username']}</div>
          <span class="badge" style="margin-top:6px;display:inline-block">GRADE {grade}</span>
          <hr style="border-color:#1e293b;margin:12px 0">
          <div style="color:#64748b;font-size:11px">Member since {join}</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:1.8rem;font-weight:900;color:{g_col};margin-top:10px">{s}/100</div>
          <div style="color:#64748b;font-size:10px;letter-spacing:2px">ECO SCORE</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:1.5rem;font-weight:900;color:#4ade80;margin-top:8px">{gp}</div>
          <div style="color:#64748b;font-size:10px;letter-spacing:2px">GREEN POINTS</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("**Preferences**")
        new_name = st.text_input("Display Name",
                                 value=st.session_state["username"], key="prof_name")
        new_home = st.selectbox("Home Location", LOC_NAMES,
                                index=LOC_NAMES.index(st.session_state["home_loc"]),
                                key="prof_home")
        modes    = ["Eco Mode", "Normal Mode", "Fast Mode"]
        new_mode = st.selectbox("Default Driving Mode", modes,
                                index=modes.index(st.session_state["driving_mode"]),
                                key="prof_mode")
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state["username"]    = new_name
            st.session_state["home_loc"]    = new_home
            st.session_state["driving_mode"]= new_mode
            st.success("✅ Preferences saved!")
            st.rerun()

    st.markdown("**My Environmental Impact**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(f"{co2} kg",            "CO2 SAVED"),              unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(f"{fuel} L",             "FUEL SAVED",   "amber"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(f"R{round(fuel*22,2)}", "MONEY SAVED",  "blue"),  unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(trips,                   "TRIPS DONE"),            unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="alert-green"><b style="color:#22c55e">Your Climate Contribution</b><br>'
                '<span style="color:#86efac;font-size:13px">By using MellowTech you help reduce urban air pollution '
                "and contribute to South Africa's climate goals. Every clean trip counts.</span></div>",
                unsafe_allow_html=True)

# ─── MAIN APP ─────────────────────────────────────────────────────────────────
def main():
    if not st.session_state["logged_in"]:
        login_page()
        return

    sidebar_nav()

    if IS_RUSH:
        st.markdown('<span style="color:#ef4444;font-size:13px;font-weight:700">⚠️ RUSH HOUR</span>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#22c55e;font-size:13px;font-weight:700">✅ TRAFFIC CLEAR</span>',
                    unsafe_allow_html=True)

    page = st.session_state["page"]
    if   page == "dashboard": page_dashboard()
    elif page == "routes":    page_routes()
    elif page == "alerts":    page_alerts()
    elif page == "analytics": page_analytics()
    elif page == "ecoscore":  page_ecoscore()
    elif page == "rewards":   page_rewards()
    elif page == "profile":   page_profile()

main()
