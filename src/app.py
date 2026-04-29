import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EV Battery Monitor 🔋", layout="wide")

# ---------------- TITLE ----------------
st.title("🔋 AI-Based EV Battery Digital Twin")
st.subheader("🔥 Fire Prediction & Safety Monitoring System")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Simulation Controls")
auto_refresh = st.sidebar.checkbox("Auto Refresh", True)

# ---------------- SENSOR SIMULATION ----------------
def get_sensor_data():
    temperature = random.uniform(25, 90)     # °C
    voltage = random.uniform(3.0, 4.2)       # V
    current = random.uniform(0, 50)          # A
    soc = random.uniform(20, 100)            # %
    return temperature, voltage, current, soc

# ---------------- PREDICTION LOGIC ----------------
def predict_status(temp, voltage, current):
    # Replace this with your LSTM model later
    if temp > 75 or current > 40:
        return "UNSAFE 🔴"
    elif temp > 60:
        return "RISK 🟠"
    else:
        return "SAFE 🟢"

# ---------------- MAIN DASHBOARD ----------------
col1, col2, col3, col4 = st.columns(4)

temp, voltage, current, soc = get_sensor_data()
status = predict_status(temp, voltage, current)

col1.metric("🌡 Temperature (°C)", f"{temp:.2f}")
col2.metric("🔌 Voltage (V)", f"{voltage:.2f}")
col3.metric("⚡ Current (A)", f"{current:.2f}")
col4.metric("🔋 State of Charge (%)", f"{soc:.2f}")

st.markdown("---")

# ---------------- PREDICTION OUTPUT ----------------
st.subheader("🤖 AI Prediction Result")

if "SAFE" in status:
    st.success(status)
elif "RISK" in status:
    st.warning(status)
else:
    st.error(status)

# ---------------- ALERT SYSTEM ----------------
st.subheader("🚨 Alerts")

if "UNSAFE" in status:
    st.error("🔥 High Risk of Battery Fire! Take immediate action!")
elif "RISK" in status:
    st.warning("⚠️ Battery entering risky condition.")
else:
    st.success("✅ Battery operating normally.")

# ---------------- AUTO REFRESH ----------------
if auto_refresh:
    time.sleep(2)
    st.rerun()
