import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Pilgrim Risk Monitor — Demo", page_icon="🕋")
st.title("🕋 Pilgrim Risk Monitor — Demo")

with open("outputs/models/rf_pilgrim_risk.pkl", "rb") as f:
    artifact = pickle.load(f)
model = artifact["model"]
le = artifact["label_encoder"]
feature_cols = artifact["feature_cols"]

with st.form("risk_form"):
    col1, col2 = st.columns(2)
    activity = col1.selectbox("Jenis Aktivitas", ["Tawaf", "Sa'i", "Resting", "Walking", "Praying"])
    crowd = col1.selectbox("Kepadatan Jamaah", ["Low", "Medium", "High"])
    age_group = col1.selectbox("Kelompok Usia", ["Under_40", "40_to_60", "Above_60"])
    experience = col1.selectbox("Pengalaman", ["First-Time", "Experienced"])
    time_of_day = col2.selectbox("Waktu", ["Fajr", "Noon", "Asr", "Maghrib", "Isha"])
    speed = col2.slider("Kecepatan Gerak (m/s)", 0.0, 2.0, 0.3)
    temp = col2.slider("Suhu (°C)", 30.0, 50.0, 38.0)
    duration = col2.slider("Durasi Aktivitas (menit)", 5, 180, 60)
    submitted = st.form_submit_button("Cek Skor Risiko")

if submitted:
    sample = {"Movement_Speed_ms": speed, "Temperature_C": temp,
              "Time_Spent_min": duration, "Pilgrim_Group_Size": 20, "Phone_Battery_Pct": 80}
    for cat, val in [("Activity_Type", activity), ("Crowd_Density", crowd),
                      ("Pilgrim_Age_Group", age_group), ("Pilgrim_Experience", experience),
                      ("Time_of_Day", time_of_day)]:
        for col in feature_cols:
            if col.startswith(cat + "_"):
                sample[col] = 1 if col == f"{cat}_{val}" else 0
    row = pd.DataFrame([sample])[feature_cols].fillna(0)
    pred = model.predict(row)[0]
    proba = model.predict_proba(row)[0]
    level = le.inverse_transform([pred])[0]
    color = {"Low": "green", "Medium": "orange", "High": "red"}[level]
    st.markdown(f"### Tingkat Risiko: :{color}[{level}]")
    st.bar_chart(dict(zip(le.classes_, proba)))