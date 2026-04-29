import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=2000, key="refresh")

st.set_page_config(layout="wide")

st.title("🚗 EV Fire Prevention Dashboard")

# SESSION
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Temp","Current","Voltage"])

if "prev_temp" not in st.session_state:
    st.session_state.prev_temp = 30

# RANDOM DATA
temp = random.uniform(30, 60)
current = random.uniform(0, 20)
voltage = random.uniform(30, 50)

rate = temp - st.session_state.prev_temp

status = "SAFE"
if rate > 5:
    status = "CRITICAL"
elif rate > 2:
    status = "WARNING"

# STORE DATA
new_data = {"Temp": temp, "Current": current, "Voltage": voltage}
st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_data])],
    ignore_index=True
).tail(50)

st.session_state.prev_temp = temp

# METRICS
col1, col2, col3 = st.columns(3)

col1.metric("Voltage (V)", f"{voltage:.2f}")
col2.metric("Current (A)", f"{current:.2f}")
col3.metric("Temperature (°C)", f"{temp:.2f}")

# STATUS
if status == "SAFE":
    st.success("Status: SAFE")
elif status == "WARNING":
    st.warning("Status: WARNING")
else:
    st.error("Status: CRITICAL 🚨")

# GRAPH
st.subheader("📈 Sensor History")

if len(st.session_state.data) > 1:
    st.line_chart(st.session_state.data)

# 3D
st.subheader("🚗 Digital Twin")

color = "green"
if status == "WARNING":
    color = "yellow"
elif status == "CRITICAL":
    color = "red"

fig = go.Figure()

fig.add_trace(go.Mesh3d(
    x=[0,1,1,0,0,1,1,0],
    y=[0,0,1,1,0,0,1,1],
    z=[0,0,0,0,1,1,1,1],
    color=color,
    opacity=0.6
))

fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    ),
    height=400
)

st.plotly_chart(fig, use_container_width=True)
