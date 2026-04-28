import requests
import time
from collections import deque
from twilio.rest import Client


client = Client(TWILIO_SID, TWILIO_AUTH)

# ================= MEMORY =================
history = {
    "temp": deque(maxlen=5),
    "gas": deque(maxlen=5),
    "current": deque(maxlen=5),
    "voltage": deque(maxlen=5)
}

last_alert_time = 0
COOLDOWN = 60

# ================= BASIC FUNCTIONS =================

def safe_float(v):
    return float(v) if v not in [None, ""] else None

def send_sms(msg):
    global last_alert_time
    now = time.time()

    if now - last_alert_time < COOLDOWN:
        return

    client.messages.create(body=msg, from_=FROM_NO, to=TO_NO)
    print("📲 SMS Sent!")
    last_alert_time = now

def predict_next(series):
    if len(series) < 2:
        return series[-1]
    trend = series[-1] - series[-2]
    return series[-1] + trend

# ================= AI NOVELTY FUNCTIONS (ADDED) =================

def root_cause(temp, current, gas):
    if temp > 50 and current > 10:
        return "Electrical Overload"
    elif temp > 50 and gas > 300:
        return "Thermal Chemical Reaction"
    elif gas > 300:
        return "Gas Leakage Risk"
    else:
        return "Normal"

def time_to_failure(temp, rate):
    if rate <= 0:
        return "Stable"
    try:
        return round((60 - temp) / rate, 2)
    except:
        return "Unknown"

def adaptive_threshold(temp_history):
    if len(temp_history) < 3:
        return 50
    return (sum(temp_history) / len(temp_history)) + 10

def confidence_score(actual, predicted):
    diff = abs(predicted - actual)
    return max(0, 100 - diff * 2)

def decision_engine(risk, confidence):
    if risk >= 7 and confidence > 70:
        return "CRITICAL"
    elif risk >= 4:
        return "WARNING"
    else:
        return "SAFE"

# ================= MAIN LOOP =================

while True:
    try:
        res = requests.get(URL)
        data = res.json()
        feeds = data.get("feeds", [])

        if not feeds:
            continue

        latest = feeds[-1]

        temp = safe_float(latest.get("field1"))
        voltage = safe_float(latest.get("field2"))
        current = safe_float(latest.get("field3"))
        rate_ts = safe_float(latest.get("field4"))
        imbalance_ts = safe_float(latest.get("field5"))
        soc_ts = safe_float(latest.get("field6"))
        gas = safe_float(latest.get("field7"))

        history["temp"].append(temp)
        history["gas"].append(gas)
        history["voltage"].append(voltage)
        history["current"].append(current)

        # 🔮 Predictions
        pred_temp = predict_next(history["temp"])
        pred_gas = predict_next(history["gas"])
        pred_voltage = predict_next(history["voltage"])
        pred_current = predict_next(history["current"])

        # 🔋 Derived
        rate = history["temp"][-1] - history["temp"][-2] if len(history["temp"]) > 1 else 0
        soc = (voltage / 4.2) * 100 if voltage else 0
        imbalance = abs(voltage - 3.7) if voltage else 0

        # 🔥 Basic Risk
        risk = 0
        if temp > 50: risk += 2
        if current > 10: risk += 2
        if gas > 300: risk += 3
        if pred_temp > 50: risk += 2

        # ================= AI NOVELTY EXECUTION =================

        cause = root_cause(temp, current, gas)
        failure_time = time_to_failure(temp, rate)
        adaptive_temp = adaptive_threshold(list(history["temp"]))
        confidence = confidence_score(temp, pred_temp)
        decision = decision_engine(risk, confidence)

        # ================= OUTPUT =================

        print("\n========= LIVE =========")
        print(f"Temp: {temp} | Pred: {pred_temp}")
        print(f"Gas: {gas} | Pred: {pred_gas}")
        print(f"Current: {current} | Pred: {pred_current}")
        print(f"Voltage: {voltage} | Pred: {pred_voltage}")

        print("\n========= DERIVED =========")
        print(f"SOC: {soc}")
        print(f"Temp Rate: {rate}")
        print(f"Imbalance: {imbalance}")

        print("\n========= AI INTELLIGENCE =========")
        print(f"Root Cause: {cause}")
        print(f"Time to Failure: {failure_time}")
        print(f"Adaptive Threshold: {adaptive_temp}")
        print(f"Confidence: {confidence}%")
        print(f"Decision: {decision}")

        print("\n========= RISK =========")
        print(f"Risk Score: {risk}")

        # 🚨 Smart Alert
        if decision == "CRITICAL":
            msg = f"""🚨 CRITICAL ALERT
Temp:{temp}->{pred_temp}
Gas:{gas}->{pred_gas}
Cause:{cause}
Time:{failure_time}
Confidence:{confidence}%
Decision:{decision}"""

            send_sms(msg)

    except Exception as e:
        print("Error:", e)

    time.sleep(20)
