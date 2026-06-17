# Siartour Pilgrim Risk Prediction
 
Proaktif risk classification (Low/Medium/High) untuk jamaah
haji/umrah berdasarkan suhu, kepadatan, kecepatan gerak, dan
profil jamaah.
 
## Hasil
- Accuracy: 89.42% | F1-Weighted: 89.38%
- ROC-AUC Macro: 0.978
- Recall (High Risk): 78.7%
 
## Validasi Anti-Overfitting
- 2 fitur kontrol (Group_Size, Battery) -> importance <0.004,
  rank #17 & #19 dari 24
- Confusion High<->Low = 0 (hanya error antar kelas bertetangga)
- SMOTE hanya pada training set
 
## Dataset
Sintetis, dikalibrasi dari:
- Memish et al. (2024) J Travel Med - DOI 10.1093/jtm/taae096
- Al-Shaery et al. (2024) IEEE Access - DOI 10.1109/ACCESS.2024.3402230
- Zittis et al. (2025) npj Natural Hazards
 
## Konteks
Ekstensi konseptual dari aplikasi Siartour (monitoring jamaah
real-time). Fungsi predict_risk() dirancang kompatibel dengan
struktur data yang dikumpulkan aplikasi.
 
## Cara Menjalankan
1. python -m venv venv && venv\Scripts\activate
2. pip install -r requirements.txt
3. python data/generate_dataset.py
4. Buka main.ipynb, Run All
