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
COOLDOWN = 60

MAX_ALERTS = 5
alert_count = 0
last_message = ""

# ================= FUNCTIONS =================

def send_sms(msg):
    global last_alert_time, alert_count, last_message

    now = time.time()

    if now - last_alert_time < COOLDOWN:
        print("Cooldown active")
        return

    if msg == last_message:
        print("Duplicate alert blocked")
        return

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


# 🔥 AI MODULES (UNCHANGED)

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


# ================= NEW FEATURE (FILTERING - ADDED ONLY) =================

def moving_average(series, window=3):
    if len(series) < window:
        return sum(series) / len(series)
    return sum(list(series)[-window:]) / window


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

    # ================= FILTER FEATURE (ALL 4 PARAMETERS ADDED) =================
    f_temp = moving_average(history["temp"])
    f_gas = moving_average(history["gas"])
    f_current = moving_average(history["current"])
    f_voltage = moving_average(history["voltage"])

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

    # ================= FINAL OUTPUT STRUCTURE =================

    print("\n================ RAW DATA =================")
    print(f"Temp: {temp} | Gas: {gas} | Current: {current} | Voltage: {voltage}")

    print("\n================ PREDICTED DATA =================")
    print(f"Temp: {pred_temp} | Gas: {pred_gas} | Current: {pred_current} | Voltage: {pred_voltage}")

    print("\n================ FILTERED DATA (NEW FEATURE) =================")
    print(f"Temp(F): {f_temp} | Gas(F): {f_gas} | Current(F): {f_current} | Voltage(F): {f_voltage}")

    print("\n================ SYSTEM HEALTH =================")
    print(f"SOC: {soc} | Temp Rate: {rate} | Imbalance: {imbalance}")

    print("\n================ AI INTELLIGENCE =================")
    print(f"Root Cause: {cause}")
    print(f"Time to Failure: {failure_time}")
    print(f"Confidence: {confidence}%")
    print(f"Decision: {decision}")

    print("\n================ RISK SCORE =================")
    print(f"Risk: {risk}")

    # ALERT
    if decision == "CRITICAL":
        msg = f"""CRITICAL ALERT
Temp:{temp}->{pred_temp}
Gas:{gas}->{pred_gas}
Risk:{risk}
Cause:{cause}
Time:{failure_time}"""

        send_sms(msg)

    time.sleep(3)
