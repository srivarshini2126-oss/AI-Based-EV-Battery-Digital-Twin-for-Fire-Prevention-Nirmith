# 🔋 AI-Based EV Battery Digital Twin for Fire Prevention - Nirmith

---

## 📘 Introduction

This project presents an intelligent **digital twin model of an electric vehicle (EV) battery** designed to predict and prevent fire hazards. The system continuously monitors critical battery parameters using sensors and real-time data acquisition. By combining IoT, data analytics, and AI-based prediction, the solution enables early detection of abnormal battery conditions and improves overall EV safety.

---

## 🎯 Objective

To design a smart and intelligent system that can:
- Monitor EV battery parameters in real time  
- Detect abnormal conditions at an early stage  
- Predict potential fire hazards using AI techniques  
- Provide timely alerts to prevent accidents  

---

## 🚀 Features

- Real-time monitoring of battery parameters  
- AI-based fire prediction system  
- Digital twin simulation of EV battery  
- IoT integration using ThingSpeak  
- SMS-based alert system using Twilio  

---

## 📊 Parameters Monitored

- Temperature  
- Current  
- Voltage  
- dT/dt (Rate of Temperature Change)  
- State of Charge (SOC)  
- Cell Imbalance  

---

## 🧩 System Architecture

This diagram illustrates the complete workflow of the system, showing how real-time sensor data is collected, processed through ESP32, transmitted to the cloud, and analyzed using AI models for early fire prediction.

<p align="center">
  <img src="docs/Architecture.jpeg" width="700"/>
</p>

---

## 🔌 Circuit Diagram

This diagram represents the hardware connections used in the project, including ESP32, temperature sensor (DHT11), voltage and current sensors, and gas sensor.

<p align="center">
  <img src="docs/circuitdiagram.jpeg" width="700"/>
</p>

---

## 📊 Prediction Output

This image shows the AI model prediction results, classifying the battery condition into:
- Safe  
- Risk  
- Unsafe  

based on real-time parameters.

<p align="center">
  <img src="docs/PredictionValue.jpeg" width="700"/>
</p>

---

## 📩 SMS Alert System

This image represents the alert system that sends notifications to the user when abnormal battery conditions are detected, enabling quick preventive action.

<p align="center">
  <img src="docs/SMSAlert.jpeg" width="700"/>
</p>

---

## 🧠 Working Principle

1. Sensors collect real-time battery data  
2. ESP32 processes and sends data to ThingSpeak  
3. Data is filtered using a moving average technique  
4. AI model (LSTM) predicts battery condition  
5. Dashboard displays live metrics and trends  
6. If abnormal condition is detected → Twilio sends SMS alert  

---

## 🎯 Conclusion

This project demonstrates an effective approach to **EV battery fire prevention** by integrating IoT, AI, and digital twin technology. The system enables real-time monitoring, early prediction, and quick alert mechanisms, making it a scalable and practical solution for enhancing EV safety.
