# ==============================
# 🔥 AI ENGINE MODULE
# ==============================

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
        time_left = (60 - temp) / rate
        return round(time_left, 2)
    except:
        return "Unknown"


def adaptive_temp_threshold(history):
    if len(history) < 3:
        return 50
    avg = sum(history) / len(history)
    return avg + 10


def confidence_score(actual, predicted):
    diff = abs(predicted - actual)
    score = max(0, 100 - diff * 2)
    return round(score, 2)


def decision_engine(risk, confidence):
    if risk >= 7 and confidence > 70:
        return "CRITICAL"
    elif risk >= 4:
        return "WARNING"
    else:
        return "SAFE"
