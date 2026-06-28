# Requirement Analysis — Pilgrim Risk Prediction System

## 1. Problem Statement
Jamaah haji/umrah, terutama kelompok usia di atas 60 tahun, rentan
mengalami kelelahan, dehidrasi, atau tersesat saat aktivitas padat
(tawaf, sa'i) di suhu ekstrem (>40°C). Dibutuhkan sistem yang dapat
mengestimasi tingkat risiko seorang jamaah secara otomatis berdasarkan
data aktivitas, agar pembimbing dapat melakukan intervensi dini.

## 2. Kebutuhan Fungsional
- FR-1: Sistem menerima input: jenis aktivitas, kecepatan gerak (m/s),
  tingkat kepadatan jamaah, suhu lingkungan (°C), kelompok usia,
  tingkat pengalaman, waktu (siang/malam), durasi aktivitas (menit).
- FR-2: Sistem mengeluarkan output klasifikasi 3 kelas: Low / Medium / High.
- FR-3: Sistem menyertakan probabilitas per kelas, bukan hanya label tunggal,
  agar pembimbing dapat menilai tingkat keyakinan prediksi.
- FR-4: Model dapat dipanggil ulang (re-usable) lewat satu fungsi
  `predict_risk()` tanpa retraining setiap kali dipakai.

## 3. Kebutuhan Non-Fungsional
- NFR-1 (Akurasi): F1-Macro minimal 0.80 pada test set
  (tercapai: lihat hasil evaluasi di notebook — ROC-AUC 0.978).
- NFR-2 (Keseimbangan kelas): karena distribusi Risk_Level tidak seimbang
  (Low jauh lebih banyak dari High), model wajib ditangani dengan teknik
  resampling (SMOTE) agar Recall kelas High tidak diabaikan.
- NFR-3 (Interoperabilitas): model harus dapat di-deploy ulang
  (serialisasi via pickle) tanpa bergantung pada notebook environment
  spesifik, supaya bisa dipanggil dari API/aplikasi lain.
- NFR-4 (Interpretability): fitur kontrol (Pilgrim_Group_Size,
  Phone_Battery_Pct) harus terbukti tidak relevan secara statistik
  (lihat permutation importance) untuk memastikan model tidak overfit
  ke fitur yang tidak punya hubungan kausal dengan risiko.

## 4. Mapping Kebutuhan → Implementasi
| Kebutuhan | Lokasi Implementasi |
|---|---|
| FR-1, FR-2, FR-3, FR-4 | `main.ipynb`, fungsi `predict_risk()` |
| NFR-1 | `main.ipynb`, evaluasi 5 metrik |
| NFR-2 | `main.ipynb`, blok SMOTE |
| NFR-3 | `outputs/models/rf_pilgrim_risk.pkl`, `code/api/main.py` |
| NFR-4 | `main.ipynb`, permutation importance |