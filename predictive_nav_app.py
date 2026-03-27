# predictive_nav_app.py
# Streamlit app simulating predictive navigation with rewards

import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --------------------------
# 🔥 HIDE TOOLBAR (ADD THIS)
# --------------------------
st.markdown("""
<style>
header, [data-testid="stHeader"], [data-testid="stToolbar"],
#MainMenu, footer {
    display: none !important;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# App Title
# --------------------------
st.title("🚗 Smart Predictive Navigation Prototype")
st.write("Simulating predictive congestion, optimized departure time, collective route shaping, and rewards!")

# --------------------------
# Simulated traffic data
# --------------------------
np.random.seed(42)
locations = ["Home", "Work", "School", "Gym", "Mall"]
hours = np.arange(6, 22)  # 6 AM to 10 PM

# Random base congestion levels (0=low, 1=high)
traffic_matrix = pd.DataFrame(
    np.random.rand(len(locations), len(hours)),
    index=locations,
    columns=hours
)

# --------------------------
# User inputs
# --------------------------
st.subheader("Your commute settings")
start = st.selectbox("Start location:", locations)
end = st.selectbox("Destination:", locations)
commute_day = st.date_input("Commute date:", datetime.date.today())
preferred_leave_time = st.slider("Preferred leave time:", 6, 22, 8)

# --------------------------
# Predictive congestion (dummy forecasting)
# --------------------------
def predict_congestion(start, end, hour):
    base = traffic_matrix.loc[start, hour]
    rush_hour = 1 if hour in [7, 8, 17, 18] else 0
    predicted = min(base + rush_hour * 0.5, 1.0)
    return predicted

st.subheader("Predicted congestion levels for your route (0=low, 1=high)")
forecast_hours = np.arange(preferred_leave_time, preferred_leave_time+3)
forecast_data = {h: predict_congestion(start, end, h) for h in forecast_hours}
st.bar_chart(pd.Series(forecast_data))

# --------------------------
# Personalized departure time optimization
# --------------------------
best_time = min(forecast_data, key=forecast_data.get)
st.success(f"✅ Optimal departure time to reduce your commute: {best_time}:00")

# --------------------------
# Collective route shaping (simulation)
# --------------------------
routes = ["Route A (fastest individually)", "Route B (less congested collectively)"]
st.subheader("Recommended route based on collective optimization")
route_choice = st.radio("Choose your route:", routes)

if route_choice == routes[1]:
    st.info("👍 You are helping reduce overall congestion!")

# --------------------------
# Rewards for coordinated behavior
# --------------------------
st.subheader("Your traffic rewards")
if route_choice == routes[1] and best_time != preferred_leave_time:
    st.balloons()
    st.success("🎉 You earned 10 reward points for coordinated commuting!")
else:
    st.info("Take the collective-optimized route to earn rewards next time.")

# --------------------------
# Footer
# --------------------------
st.write("---")
st.write("⚠️ This is a **simulation prototype**. Real predictive routing requires live GPS, weather, and historical traffic data.")
