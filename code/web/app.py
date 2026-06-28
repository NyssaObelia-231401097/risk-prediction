import streamlit as st
import requests

st.set_page_config(page_title="Risk Monitor — Web Demo", page_icon="🕋")
st.title("🕋 Risk Monitor — Web Demo")
st.caption("Demo independen: mengonsumsi model risk-prediction lewat REST API")

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
    payload = {
        "activity": activity, "speed_ms": speed, "crowd_density": crowd,
        "temperature": temp, "age_group": age_group, "experience": experience,
        "time_of_day": time_of_day, "time_spent_min": duration,
    }
    res = requests.post("http://localhost:8000/predict", json=payload).json()
    level = res["risk_level"]
    color = {"Low": "green", "Medium": "orange", "High": "red"}[level]
    st.markdown(f"### Tingkat Risiko: :{color}[{level}]")
    st.bar_chart(res["probabilities"])