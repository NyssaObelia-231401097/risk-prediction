import numpy as np
import pandas as pd

np.random.seed(42)
N = 12_000          # jumlah jamaah simulasi
RISK_NOISE_STD = 0.3  # hasil sweep eksperimen, lihat Bab 6.3 dokumen

# ---------------------------------------------------------
# 0.2 - Activity_Type, Crowd_Density, Movement_Speed
# ---------------------------------------------------------
activity_types = ['Tawaf', 'Sai', 'Prayer', 'Walking', 'Resting']
activity_probs = [0.15, 0.12, 0.20, 0.35, 0.18]
Activity_Type = np.random.choice(activity_types, N, p=activity_probs)

# Tawaf & Prayer punya probabilitas lebih tinggi Crowd=High
crowd_levels = ['Low', 'Medium', 'High']
crowd_base = np.random.choice(crowd_levels, N, p=[0.30, 0.45, 0.25])
crowd_adj = crowd_base.copy()
for i in range(N):
    if Activity_Type[i] in ['Tawaf', 'Prayer'] and np.random.random() < 0.5:
        crowd_adj[i] = 'High'
Crowd_Density = crowd_adj

# Kecepatan dikalibrasi per aktivitas (Al-Shaery et al., 2024)
speed_map = {'Tawaf': (0.3, 0.8), 'Sai': (0.8, 1.5), 'Prayer': (0.0, 0.1),
             'Walking': (0.5, 1.2), 'Resting': (0.0, 0.3)}
Movement_Speed = np.array([np.random.uniform(*speed_map[a])
                            for a in Activity_Type]).round(3)

# ---------------------------------------------------------
# 0.3 - Temperature, Profil Jamaah, Waktu
# ---------------------------------------------------------
# Suhu Mekkah: Zittis et al. (2025), Memish et al. (2024)
Temperature = np.random.normal(42, 4, N).clip(32, 52).round(1)

Pilgrim_Experience = np.random.choice(
    ['First-Time', 'Experienced'], N, p=[0.60, 0.40])

# Distribusi usia jamaah Indonesia (Kemenag RI)
Pilgrim_Age_Group = np.random.choice(
    ['Under_40', '40_to_60', 'Above_60'], N, p=[0.20, 0.55, 0.25])

time_slots = ['Fajr', 'Morning', 'Noon', 'Afternoon', 'Maghrib', 'Night']
Time_of_Day = np.random.choice(
    time_slots, N, p=[0.10, 0.20, 0.18, 0.22, 0.15, 0.15])

time_spent_map = {'Tawaf': (30, 90), 'Sai': (45, 90), 'Prayer': (10, 30),
                   'Walking': (5, 30), 'Resting': (15, 120)}
Time_Spent = np.array([np.random.uniform(*time_spent_map[a])
                        for a in Activity_Type]).round(1)

# ---------------------------------------------------------
# 0.4 - Dua Fitur Kontrol (Anti-Halu)
# ---------------------------------------------------------
# SENGAJA tidak masuk rumus skor risiko apapun
Pilgrim_Group_Size = np.random.randint(5, 51, N)
Phone_Battery_Pct = np.random.randint(5, 101, N)

# ---------------------------------------------------------
# 0.5 - Rumus Skor Risiko
# ---------------------------------------------------------
def compute_risk_score(i):
    score = 0.0

    if Crowd_Density[i] == 'High' and Movement_Speed[i] < 0.2:
        score += 2.5
    elif Crowd_Density[i] == 'High' and Movement_Speed[i] < 0.4:
        score += 1.5

    if Temperature[i] > 46:
        score += 3.0
    elif Temperature[i] > 44:
        score += 2.0
    elif Temperature[i] > 42:
        score += 1.0

    if Pilgrim_Age_Group[i] == 'Above_60':
        score += 1.5
    elif Pilgrim_Age_Group[i] == '40_to_60':
        score += 0.5

    if Pilgrim_Experience[i] == 'First-Time':
        score += 1.0
    if Time_of_Day[i] in ['Noon', 'Afternoon']:
        score += 1.0

    if Activity_Type[i] == 'Tawaf' and Crowd_Density[i] == 'High':
        score += 1.5

    if Activity_Type[i] not in ['Resting', 'Prayer'] and Time_Spent[i] > 75:
        score += 1.0

    # LAPIS 1 anti-halu: noise faktor tak terukur
    score += np.random.normal(0, RISK_NOISE_STD)
    return max(score, 0)


risk_scores = np.array([compute_risk_score(i) for i in range(N)])


def score_to_label(s):
    if s >= 6.0:
        return 'High'
    elif s >= 3.5:
        return 'Medium'
    return 'Low'


Risk_Level = np.array([score_to_label(s) for s in risk_scores])

# ---------------------------------------------------------
# Gabungkan jadi DataFrame & simpan ke CSV
# ---------------------------------------------------------
df = pd.DataFrame({
    'Activity_Type': Activity_Type,
    'Movement_Speed_ms': Movement_Speed,
    'Crowd_Density': Crowd_Density,
    'Temperature_C': Temperature,
    'Pilgrim_Age_Group': Pilgrim_Age_Group,
    'Pilgrim_Experience': Pilgrim_Experience,
    'Time_of_Day': Time_of_Day,
    'Time_Spent_min': Time_Spent,
    'Pilgrim_Group_Size': Pilgrim_Group_Size,
    'Phone_Battery_Pct': Phone_Battery_Pct,
    'Risk_Level': Risk_Level,
})

df.to_csv('data/pilgrim_risk_dataset.csv', index=False)

print(f'Dataset berhasil dibuat: {df.shape[0]} baris, {df.shape[1]} kolom')
print(df['Risk_Level'].value_counts())