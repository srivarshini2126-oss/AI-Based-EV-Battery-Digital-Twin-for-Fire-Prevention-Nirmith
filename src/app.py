import streamlit as st
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=2000, key="refresh")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="EV Dashboard", layout="wide")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0e1117;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
h1 {
    text-align: center;
    color: #00FFAA;
}
[data-testid="stMetricLabel"] {
    font-size: 16px;
    color: #AAAAAA;
}
[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🚗 EV Battery Monitoring Dashboard")

# ---------- SESSION STORAGE ----------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Temp", "dT/dt", "Voltage", "Current", "SOC", "Imbalance", "Resistance"
    ])

if "prev_temp" not in st.session_state:
    st.session_state.prev_temp = 30

# ---------- RANDOM DATA ----------
temp = random.uniform(30, 60)
voltage = random.uniform(300, 420)
current = random.uniform(0, 150)
soc = random.uniform(20, 100)
imbalance = random.uniform(0, 5)
resistance = random.uniform(0.01, 0.1)

# ---------- RATE ----------
dTdt = temp - st.session_state.prev_temp

# ---------- STORE ----------
new_row = {
    "Temp": temp,
    "dT/dt": dTdt,
    "Voltage": voltage,
    "Current": current,
    "SOC": soc,
    "Imbalance": imbalance,
    "Resistance": resistance
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_row])],
    ignore_index=True
).tail(50)

st.session_state.prev_temp = temp

# ---------- METRICS ----------
col1, col2, col3, col4 = st.columns(4)
col5, col6, col7 = st.columns(3)

col1.metric("🌡 Temp (°C)", f"{temp:.2f}")
col2.metric("⚡ dT/dt", f"{dTdt:.2f}")
col3.metric("🔋 Voltage (V)", f"{voltage:.2f}")
col4.metric("🔌 Current (A)", f"{current:.2f}")

col5.metric("🔋 SOC (%)", f"{soc:.2f}")
col6.metric("⚖ Imbalance", f"{imbalance:.2f}")
col7.metric("🧪 Resistance", f"{resistance:.3f}")

# ---------- GRAPH ----------
st.subheader("📈 Parameter Trends")
st.line_chart(st.session_state.data)

# ---------- RISK ----------
risk = 0

if temp > 55:
    risk += 2
if dTdt > 3:
    risk += 2
if current > 120:
    risk += 2
if imbalance > 3:
    risk += 1

# ---------- STATUS ----------
if risk >= 5:
    st.error("🔥 HIGH FIRE RISK")
elif risk >= 3:
    st.warning("⚠️ WARNING")
else:
    st.success("✅ SAFE")

# ---------- 3D MODEL ----------
st.subheader("🚗 Digital Twin (3D EV)")

components.html("""
<div style="width:100%; height:500px;">
<iframe 
    title="EV Car"
    frameborder="0"
    allowfullscreen
    allow="autoplay; fullscreen; xr-spatial-tracking"
    width="100%"
    height="100%"
    src="https://sketchfab.com/models/8be255da521b46d283ddc21803484c3b/embed?autostart=1&ui_controls=0&ui_infos=0&ui_watermark=0">
</iframe>
</div>
""", height=520)
