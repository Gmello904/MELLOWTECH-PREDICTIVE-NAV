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
# SESSION STATE — Login
# ------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "home_location" not in st.session_state:
    st.session_state.home_location = "Home"
if "theme" not in st.session_state:
    st.session_state.theme = "Cyan"

# ------------------------------------------------
# LOADING SCREEN (first load only)
# ------------------------------------------------
if "loaded" not in st.session_state:
    with st.spinner("Launching MELLOWTECH AI Engine..."):
        time.sleep(1)
    st.session_state.loaded = True

# ------------------------------------------------
# THEME COLORS
# ------------------------------------------------
themes = {
    "Cyan":    {"accent": "#00ffff", "glow": "#00cfff", "btn": "#0ea5e9"},
    "Purple":  {"accent": "#c084fc", "glow": "#a855f7", "btn": "#7c3aed"},
    "Green":   {"accent": "#4ade80", "glow": "#22c55e", "btn": "#16a34a"},
    "Orange":  {"accent": "#fb923c", "glow": "#f97316", "btn": "#ea580c"},
}
acc  = themes[st.session_state.theme]["accent"]
glow = themes[st.session_state.theme]["glow"]
btn  = themes[st.session_state.theme]["btn"]

# ------------------------------------------------
# PREMIUM STYLE
# ------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap');

.stApp {{
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
    font-family: 'Rajdhani', sans-serif;
}}

#MainMenu {{visibility: hidden;}}
footer     {{visibility: hidden;}}
header     {{background: transparent;}}

[data-testid="stSidebar"] {{
    background: #020617;
    border-right: 1px solid #1e293b;
}}

@media (max-width: 768px) {{
    [data-testid="stSidebar"] {{ width: 260px !important; }}
    div[role="radiogroup"] label {{ font-size: 20px; padding: 18px; }}
}}

div[role="radiogroup"] label {{
    padding: 14px;
    border-radius: 12px;
    color: silver;
    font-size: 17px;
    display: block;
    font-family: 'Rajdhani', sans-serif;
}}
div[role="radiogroup"] label:hover {{
    background: #0f172a;
    color: white;
}}
div[role="radiogroup"] label[data-selected="true"] {{
    background: #111827;
    color: {acc};
    border-left: 4px solid {acc};
}}

.title {{
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: {acc};
    text-shadow: 0 0 20px {glow}, 0 0 40px {glow};
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 4px;
    margin-bottom: 4px;
}}

.subtitle {{
    text-align: center;
    color: #64748b;
    font-size: 14px;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 30px;
}}

.kpi-card {{
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {acc}, transparent);
}}

.kpi-value {{
    font-size: 32px;
    font-weight: 900;
    color: {acc};
    font-family: 'Orbitron', sans-serif;
}}

.kpi-label {{
    font-size: 12px;
    letter-spacing: 3px;
    color: #64748b;
    text-transform: uppercase;
    margin-top: 4px;
}}

.traffic-card {{
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 12px;
}}

.login-box {{
    max-width: 400px;
    margin: 60px auto;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
}}

.badge {{
    display: inline-block;
    background: {acc}22;
    color: {acc};
    border: 1px solid {acc}55;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    letter-spacing: 2px;
}}

.stTextInput > div > div > input {{
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Rajdhani', sans-serif !important;
}}

.stSelectbox > div > div {{
    background: #1e293b !important;
    border-radius: 10px !important;
}}

div[data-testid="stMetricValue"] {{
    color: {acc} !important;
    font-family: 'Orbitron', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# ================================================
# LOGIN GATE
# ================================================
if not st.session_state.logged_in:
    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Predictive Traffic Intelligence</div>", unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{acc};font-family:Orbitron;text-align:center;'>Sign In</h3>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your name")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Launch Dashboard", use_container_width=True):
            if username.strip() == "":
                st.error("Please enter a username.")
            elif password == "":
                st.error("Please enter a password.")
            else:
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.success(f"Welcome, {username}!")
                time.sleep(0.5)
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569;font-size:12px;text-align:center;'>Demo: any username + any password</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ================================================
# SIDEBAR (after login)
# ================================================
st.sidebar.markdown(f"<div style='font-family:Orbitron;color:{acc};font-size:18px;font-weight:900;padding:10px 0;letter-spacing:2px;'>MELLOWTECH</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='badge'>● ONLINE</div><br><br>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:#64748b;font-size:13px;'>👤 {st.session_state.username}</p>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "",
    ["🏠 Dashboard", "🚦 Traffic", "🧭 Navigation", "📊 Analytics", "👤 Profile"]
)

if st.sidebar.button("🔓 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# ================================================
# DASHBOARD PAGE
# ================================================
if menu == "🏠 Dashboard":

    st.markdown("<div class='title'>MELLOWTECH</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Predictive Traffic Intelligence</div>", unsafe_allow_html=True)

    time_now   = dt.now().strftime("%H:%M:%S")
    date_today = dt.now().strftime("%d %b %Y")
    hour_now   = dt.now().hour
    rush_hour  = "YES ⚠️" if (7 <= hour_now <= 9 or 16 <= hour_now <= 18) else "NO ✅"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>{time_now}</div>
            <div class='kpi-label'>Current Time</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>ONLINE</div>
            <div class='kpi-label'>System Status</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>ACTIVE</div>
            <div class='kpi-label'>AI Engine</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>{rush_hour}</div>
            <div class='kpi-label'>Rush Hour</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"✅ Predictive Traffic Intelligence Running — {date_today}")

    st.markdown("---")
    st.subheader("📡 Live City Traffic Pulse")

    locations = ["Home", "Work", "School", "Mall", "Hospital", "Airport"]
    np.random.seed(hour_now)
    congestion = np.random.randint(10, 90, len(locations))
    congestion = [min(100, c + 25) if (7 <= hour_now <= 9 or 16 <= hour_now <= 18) else c for c in congestion]

    pulse_df = pd.DataFrame({"Location": locations, "Congestion %": congestion})
    st.bar_chart(pulse_df.set_index("Location"))

# ================================================
# TRAFFIC PAGE
# ================================================
elif menu == "🚦 Traffic":

    st.markdown(f"<h1 style='font-family:Orbitron;color:{acc};'>Traffic Prediction</h1>", unsafe_allow_html=True)

    locations = ["Home", "Work", "School", "Mall", "Hospital", "Airport"]

    col1, col2, col3 = st.columns(3)
    with col1:
        start = st.selectbox("🟢 Start", locations)
    with col2:
        end   = st.selectbox("🔴 Destination", [l for l in locations if l != start])
    with col3:
        leave = st.slider("🕐 Departure Hour", 6, 22, dt.now().hour)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI Simulation
    np.random.seed(leave + 42)
    base = np.random.randint(10, 70, len(locations))
    congestion = [
        min(100, c + 30) if 7 <= leave <= 9 or 16 <= leave <= 18 else c
        for c in base
    ]

    df = pd.DataFrame({"Location": locations, "Congestion %": congestion})

    # Traffic light cards
    st.subheader("🚦 AI Traffic Status")
    cols = st.columns(3)
    for i, row in df.iterrows():
        level = row["Congestion %"]
        if level > 70:
            emoji, status, color = "🔴", "Heavy Traffic", "#ef4444"
        elif level > 40:
            emoji, status, color = "🟡", "Moderate Flow", "#f59e0b"
        else:
            emoji, status, color = "🟢", "Smooth Flow", "#22c55e"

        with cols[i % 3]:
            st.markdown(f"""
            <div style='background:#0f172a;border:1px solid #1e293b;border-left:4px solid {color};
                        border-radius:12px;padding:14px;margin-bottom:12px;'>
                <div style='font-size:22px;'>{emoji} <b>{row["Location"]}</b></div>
                <div style='color:{color};font-size:14px;letter-spacing:1px;'>{status}</div>
                <div style='font-size:28px;font-family:Orbitron;color:{color};'>{level}%</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📈 Congestion Chart")
        st.bar_chart(df.set_index("Location"))
    with col_b:
        st.subheader("📋 Data Table")
        st.dataframe(df, use_container_width=True, hide_index=True)

    best = df.loc[df["Congestion %"].idxmin(), "Location"]
    worst = df.loc[df["Congestion %"].idxmax(), "Location"]
    st.success(f"✅ Best Route via: **{best}** — Lowest congestion at {df['Congestion %'].min()}%")
    st.warning(f"⚠️ Avoid: **{worst}** — Highest congestion at {df['Congestion %'].max()}%")

# ================================================
# NAVIGATION PAGE
# ================================================
elif menu == "🧭 Navigation":

    st.markdown(f"<h1 style='font-family:Orbitron;color:{acc};'>Live Navigation</h1>", unsafe_allow_html=True)

    st.info("📍 Map centred on Pretoria, South Africa — adjust waypoints below")

    locations_coords = {
        "Home":        (-25.7461, 28.1881),
        "Work":        (-25.7580, 28.1890),
        "School":      (-25.7400, 28.2100),
        "Mall":        (-25.7650, 28.3120),
        "Hospital":    (-25.7320, 28.2280),
        "Airport":     (-25.9180, 28.3820),
    }

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("📍 Origin", list(locations_coords.keys()))
    with col2:
        dest   = st.selectbox("🏁 Destination", [k for k in locations_coords if k != origin])

    waypoints = st.multiselect("➕ Add Waypoints (optional)", [k for k in locations_coords if k not in [origin, dest]])

    route = [origin] + waypoints + [dest]
    route_coords = [locations_coords[r] for r in route]

    map_df = pd.DataFrame(route_coords, columns=["lat", "lon"])

    st.map(map_df, zoom=12)

    st.markdown("### 🗺️ Route Summary")
    for i, stop in enumerate(route):
        icon = "🟢" if i == 0 else ("🏁" if i == len(route) - 1 else "📍")
        lat, lon = locations_coords[stop]
        st.markdown(f"{icon} **{stop}** — `{lat:.4f}, {lon:.4f}`")

    # Estimated travel info (simulated)
    np.random.seed(len(route))
    dist_km = round(np.random.uniform(3, 25) * len(route) / 2, 1)
    mins    = int(dist_km * 2.2 + np.random.randint(2, 10))

    col_d, col_t = st.columns(2)
    col_d.metric("📏 Est. Distance", f"{dist_km} km")
    col_t.metric("⏱️ Est. Travel Time", f"{mins} min")

# ================================================
# ANALYTICS PAGE
# ================================================
elif menu == "📊 Analytics":

    st.markdown(f"<h1 style='font-family:Orbitron;color:{acc};'>Traffic Analytics</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Hourly Trends", "📊 Location Stats", "🔥 Heatmap"])

    with tab1:
        st.subheader("Hourly Traffic Trends (24h)")
        hours = list(range(0, 24))
        np.random.seed(7)
        base_flow = np.random.randint(20, 60, 24)
        rush_boost = [30 if (7 <= h <= 9 or 16 <= h <= 18) else 0 for h in hours]
        speed      = [max(10, 80 - b - r + np.random.randint(-5, 5)) for b, r in zip(base_flow, rush_boost)]
        congestion = [min(100, b + r + np.random.randint(-5, 5)) for b, r in zip(base_flow, rush_boost)]
        flow       = [max(5, 60 - c // 3 + np.random.randint(-3, 3)) for c in congestion]

        hourly_df = pd.DataFrame({
            "Hour":       hours,
            "Speed (km/h)":  speed,
            "Congestion %":  congestion,
            "Traffic Flow":  flow
        }).set_index("Hour")

        st.line_chart(hourly_df)

        peak_hour = hours[np.argmax(congestion)]
        st.info(f"🔺 Peak congestion at **{peak_hour}:00** with **{max(congestion)}%** congestion")

    with tab2:
        st.subheader("Location Performance Stats")
        locations = ["Home", "Work", "School", "Mall", "Hospital", "Airport"]
        np.random.seed(99)
        stats_df = pd.DataFrame({
            "Location":      locations,
            "Avg Speed":     np.random.randint(30, 80, 6),
            "Avg Congestion": np.random.randint(15, 75, 6),
            "Incidents":     np.random.randint(0, 10, 6),
            "Flow Score":    np.random.randint(50, 100, 6),
        })

        col_a, col_b = st.columns(2)
        with col_a:
            st.bar_chart(stats_df.set_index("Location")[["Avg Speed", "Avg Congestion"]])
        with col_b:
            st.dataframe(stats_df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Weekly Traffic Heatmap (Simulated)")
        days   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        h_hrs  = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        np.random.seed(42)
        heat   = np.random.randint(10, 90, (len(days), len(h_hrs)))
        for i, (r, d) in enumerate(zip(heat, days)):
            heat[i] = [min(100, v + 30) if h in [7,8,17,18] else v for v, h in zip(r, h_hrs)]

        heat_df = pd.DataFrame(heat, index=days, columns=[f"{h}:00" for h in h_hrs])
        st.dataframe(heat_df.style.background_gradient(cmap="RdYlGn_r"), use_container_width=True)

# ================================================
# PROFILE PAGE
# ================================================
elif menu == "👤 Profile":

    st.markdown(f"<h1 style='font-family:Orbitron;color:{acc};'>User Profile</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div style='background:#0f172a;border:1px solid #1e293b;border-radius:20px;padding:30px;text-align:center;'>
            <div style='font-size:64px;'>👤</div>
            <div style='font-size:24px;font-family:Orbitron;color:{acc};margin-top:10px;'>{st.session_state.username}</div>
            <div class='badge' style='margin-top:8px;'>MELLOWTECH USER</div>
            <hr style='border-color:#1e293b;margin:16px 0;'>
            <div style='color:#64748b;font-size:13px;'>Member since {dt.now().strftime("%b %Y")}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("⚙️ Preferences")

        new_username = st.text_input("Display Name", value=st.session_state.username)
        home_loc     = st.selectbox("🏠 Home Location", ["Home","Work","School","Mall","Hospital","Airport"],
                                    index=["Home","Work","School","Mall","Hospital","Airport"].index(st.session_state.home_location))
        theme_choice = st.selectbox("🎨 Theme Color", list(themes.keys()),
                                    index=list(themes.keys()).index(st.session_state.theme))

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Preferences", use_container_width=True):
            st.session_state.username      = new_username
            st.session_state.home_location = home_loc
            st.session_state.theme         = theme_choice
            st.success("✅ Preferences saved!")
            time.sleep(0.5)
            st.rerun()

    st.markdown("---")
    st.subheader("📊 My Activity Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Routes Searched", "24")
    c2.metric("Trips Saved",     "8")
    c3.metric("Alerts Received", "12")
    c4.metric("Avg Commute",     "32 min")
