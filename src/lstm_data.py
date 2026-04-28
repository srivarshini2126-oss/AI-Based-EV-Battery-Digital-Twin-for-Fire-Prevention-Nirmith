import pandas as pd
import time
from collections import deque
from twilio.rest import Client

# ================= CONFIG =================
CSV_FILE = "data.csv"

# ================= MEMORY =================
history = {
    "temp": deque(maxlen=5),
    "gas": deque(maxlen=5),
    "current": deque(maxlen=5),
    "voltage": deque(maxlen=5)
}

last_alert_time = 0
COOLDOWN = 60   # seconds

# 🔥 NEW LIMIT CONTROLS
MAX_ALERTS = 5
alert_count = 0
last_message = ""

# ================= FUNCTIONS =================

def send_sms(msg):
    global last_alert_time, alert_count, last_message

    now = time.time()

    # ⏳ Cooldown check
    if now - last_alert_time < COOLDOWN:
        print("Cooldown active")
        return

    # 🔁 Duplicate prevention
    if msg == last_message:
        print("Duplicate alert blocked")
        return

    # 🚫 Max alert limit
    if alert_count >= MAX_ALERTS:
        print("Max alert limit reached")
        return

    try:
        client.messages.create(
            body=msg,
            from_=FROM_NO,
            to=TO_NO
        )
        print("SMS SENT")

        last_alert_time = now
        last_message = msg
        alert_count += 1

    except Exception as e:
        print("Twilio Error:", e)


def predict_next(series):
    if len(series) < 2:
        return series[-1]
    trend = series[-1] - series[-2]
    return series[-1] + trend


# 🔥 AI NOVELTY MODULES

def root_cause(temp, current, gas):
    if temp > 50 and current > 10:
        return "Electrical Overload"
    elif temp > 50 and gas > 300:
        return "Thermal Chemical Risk"
    return "Normal"


def time_to_failure(temp, rate):
    if rate <= 0:
        return "Stable"
    return round((60 - temp) / rate, 2)


def confidence_score(actual, predicted):
    return max(0, 100 - abs(predicted - actual) * 2)


def decision_engine(risk, confidence):
    if risk >= 7 and confidence > 60:
        return "CRITICAL"
    elif risk >= 4:
        return "WARNING"
    return "SAFE"


def calculate_risk(temp, current, voltage, gas,
                   pred_temp, pred_gas,
                   soc, rate, imbalance):

    risk = 0

    if temp > 50: risk += 2
    if current > 10: risk += 2
    if voltage > 240 or voltage < 180: risk += 2
    if gas > 300: risk += 3

    if pred_temp > 50: risk += 2
    if pred_gas > 300: risk += 3

    if soc < 20: risk += 2
    if rate > 5: risk += 2
    if imbalance > 0.5: risk += 2

    return risk


# ================= MAIN =================

df = pd.read_csv(CSV_FILE)

for index, row in df.iterrows():

    temp = row["temp"]
    current = row["current"]
    voltage = row["voltage"]
    rate = row["temp_rate"]
    imbalance = row["imbalance"]
    soc = row["soc"]
    gas = row["gas"]

    # update history
    history["temp"].append(temp)
    history["gas"].append(gas)
    history["current"].append(current)
    history["voltage"].append(voltage)

    # predictions
    pred_temp = predict_next(history["temp"])
    pred_gas = predict_next(history["gas"])
    pred_current = predict_next(history["current"])
    pred_voltage = predict_next(history["voltage"])

    # risk
    risk = calculate_risk(temp, current, voltage, gas,
                          pred_temp, pred_gas,
                          soc, rate, imbalance)

    # AI ENGINE
    cause = root_cause(temp, current, gas)
    failure_time = time_to_failure(temp, rate)
    confidence = confidence_score(temp, pred_temp)
    decision = decision_engine(risk, confidence)

    # ================= OUTPUT =================
    print("\n====== DATA FROM CSV ======")
    print(f"Temp: {temp} → {pred_temp}")
    print(f"Gas: {gas} → {pred_gas}")
    print(f"Current: {current} → {pred_current}")
    print(f"Voltage: {voltage} → {pred_voltage}")

    print("\n====== SYSTEM HEALTH ======")
    print(f"SOC: {soc}")
    print(f"Temp Rate: {rate}")
    print(f"Imbalance: {imbalance}")

    print("\n====== AI INTELLIGENCE ======")
    print(f"Root Cause: {cause}")
    print(f"Time to Failure: {failure_time}")
    print(f"Confidence: {confidence}%")
    print(f"Decision: {decision}")

    print(f"\n🔥 Risk Score: {risk}")

    # ALERT
    if decision == "CRITICAL":
        msg = f"""CRITICAL ALERT
Temp:{temp}->{pred_temp}
Gas:{gas}->{pred_gas}
Cause:{cause}
Time:{failure_time}
Risk:{risk}"""

        send_sms(msg)

    time.sleep(3)
