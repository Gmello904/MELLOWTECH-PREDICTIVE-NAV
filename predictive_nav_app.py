import streamlit as st

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="MELLOWTECH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# SESSION LOGIN STATE
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------
# MODERN CSS DESIGN
# ----------------------------
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#05070d,#0b132b);
    color:white;
    overflow-x:hidden;
}

/* Remove Streamlit menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* LOGIN CARD */
.login-card{
    max-width:420px;
    margin:auto;
    margin-top:120px;
    background:#111827;
    padding:40px;
    border-radius:18px;
    box-shadow:0 0 40px rgba(0,255,200,0.15);
}

/* APP HEADER */
.app-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#00ffd0;
    margin-bottom:20px;
}

/* SWIPE CONTAINER */
.swipe-container{
    display:flex;
    overflow-x:auto;
    scroll-snap-type:x mandatory;
    gap:20px;
    padding:20px;
}

/* EACH PAGE */
.page{
    flex:0 0 90%;
    height:75vh;
    background:#111827;
    border-radius:20px;
    padding:30px;
    scroll-snap-align:center;
    box-shadow:0 0 25px rgba(0,255,200,0.1);
}

/* Hide scrollbar */
.swipe-container::-webkit-scrollbar{
    display:none;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOGIN PAGE
# ----------------------------
if not st.session_state.logged_in:

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align:center;color:#00ffd0;'>MELLOWTECH</h1>",
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid login")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# MAIN APP AFTER LOGIN
# ----------------------------
else:

    st.markdown('<div class="app-title">MELLOWTECH</div>', unsafe_allow_html=True)

    # Swipe Layout
    st.markdown("""
    <div class="swipe-container">

        <div class="page">
            <h2>🏠 Dashboard</h2>
            <p>Welcome to MELLOWTECH Cybersecurity Platform.</p>
            <p>Monitor threats, analytics and system performance.</p>
        </div>

        <div class="page">
            <h2>🧠 AI Security</h2>
            <p>AI Threat Detection Engine.</p>
            <ul>
            <li>Malware Prediction</li>
            <li>Network Monitoring</li>
            <li>Risk Scoring</li>
            </ul>
        </div>

        <div class="page">
            <h2>📊 Analytics</h2>
            <p>Real-time Cybersecurity Intelligence Dashboard.</p>
            <p>Visualise attack patterns and vulnerabilities.</p>
        </div>

        <div class="page">
            <h2>⚙ Settings</h2>
            <p>User profile, integrations and configurations.</p>
        </div>

    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
