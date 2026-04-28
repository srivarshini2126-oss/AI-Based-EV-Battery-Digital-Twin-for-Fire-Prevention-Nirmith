import requests
import time
from collections import deque
from twilio.rest import Client
# ================= CONFIG =================

FROM_NO = "+19785413833"
TO_NO = "+917397048336"

URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=10"

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

# ================= FUNCTIONS =================

def safe_float(v):
    return float(v) if v not in [None, ""] else None


def send_sms(msg):
    global last_alert_time
    now = time.time()

    if now - last_alert_time < COOLDOWN:
        print("⏳ Cooldown active")
        return

    client.messages.create(body=msg, from_=FROM_NO, to=TO_NO)
    print("📲 SMS Sent!")
    last_alert_time = now


def predict_next(series):
    if len(series) < 2:
        return series[-1]
    trend = series[-1] - series[-2]
    return series[-1] + trend


# ================= DATA FETCH =================

def get_data():
    try:
        res = requests.get(URL)
        data = res.json()
        feeds = data.get("feeds", [])

        if not feeds:
            return None

        latest = feeds[-1]

        # 🔹 Read all 7 fields from ThingSpeak
        temp = safe_float(latest.get("field1"))
        current = safe_float(latest.get("field2"))
        voltage = safe_float(latest.get("field3"))
        temp_rate_ts = safe_float(latest.get("field4"))
        imbalance_ts = safe_float(latest.get("field5"))
        soc_ts = safe_float(latest.get("field6"))
        gas = safe_float(latest.get("field7"))

        return temp, current, voltage, temp_rate_ts, imbalance_ts, soc_ts, gas

    except Exception as e:
        print("Error:", e)
        return None


# ================= DERIVED =================

def calc_temp_rate():
    if len(history["temp"]) < 2:
        return 0
    return history["temp"][-1] - history["temp"][-2]

def calc_imbalance(voltage):
    return abs(voltage - 3.7)

def calc_soc(voltage):
    return (voltage / 4.2) * 100


# ================= RISK =================

def calculate_risk(temp, current, voltage, gas,
                   pred_temp, pred_gas, pred_current, pred_voltage,
                   soc, rate, imbalance):

    risk = 0

    # Current values
    if temp > 50: risk += 2
    if current > 10: risk += 2
    if voltage > 250 or voltage < 180: risk += 2
    if gas > 300: risk += 3

    # Predictions
    if pred_temp > 50: risk += 2
    if pred_gas > 300: risk += 3
    if pred_current > 10: risk += 1
    if pred_voltage > 250 or pred_voltage < 180: risk += 1

    # Derived
    if soc < 20: risk += 2
    if rate > 5: risk += 2
    if imbalance > 0.5: risk += 2

    return risk


# ================= MAIN LOOP =================

while True:
    data = get_data()

    if data:
        temp, current, voltage, temp_rate_ts, imbalance_ts, soc_ts, gas = data

        # Update history
        history["temp"].append(temp)
        history["gas"].append(gas)
        history["current"].append(current)
        history["voltage"].append(voltage)

        # 🔮 Predictions
        pred_temp = predict_next(history["temp"])
        pred_gas = predict_next(history["gas"])
        pred_current = predict_next(history["current"])
        pred_voltage = predict_next(history["voltage"])

        # 🔋 Derived (recalculate for reliability)
        rate = calc_temp_rate()
        imbalance = calc_imbalance(voltage)
        soc = calc_soc(voltage)

        # 🔥 Risk
        risk = calculate_risk(temp, current, voltage, gas,
                              pred_temp, pred_gas, pred_current, pred_voltage,
                              soc, rate, imbalance)

        # ================= OUTPUT =================
        print("\n========= LIVE DATA =========")
        print(f"Temp: {temp}")
        print(f"Current: {current}")
        print(f"Voltage: {voltage}")
        print(f"Gas: {gas}")

        print("\n========= PREDICTIONS =========")
        print(f"Next Temp: {pred_temp}")
        print(f"Next Gas: {pred_gas}")
        print(f"Next Current: {pred_current}")
        print(f"Next Voltage: {pred_voltage}")

        print("\n========= DERIVED =========")
        print(f"SOC: {soc:.2f}")
        print(f"Temp Rate: {rate}")
        print(f"Imbalance: {imbalance}")

        print("\n========= RISK =========")
        print(f"Risk Score: {risk}")

        # 🚨 Alert
        if risk >= 6:
            msg = f"""ALERT!
Temp:{temp}→{pred_temp}
Gas:{gas}→{pred_gas}
Curr:{current}→{pred_current}
Volt:{voltage}→{pred_voltage}
SOC:{soc:.1f}
Risk:{risk}"""

            send_sms(msg)

    time.sleep(20)
