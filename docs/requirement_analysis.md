# Requirement Analysis — Pilgrim Risk Prediction System

## 1. Problem Statement

Jamaah haji/umrah, terutama kelompok usia di atas 60 tahun, rentan mengalami kelelahan, dehidrasi, atau tersesat saat melakukan aktivitas padat (tawaf, sa'i) dalam suhu ekstrem (>40°C). Oleh karena itu, dibutuhkan sebuah sistem yang dapat mengestimasi tingkat risiko seorang jamaah secara otomatis berdasarkan data aktivitas, sehingga pembimbing dapat melakukan intervensi sejak dini.

## 2. Kebutuhan Fungsional

**FR-1 — Input Data Aktivitas**
Sistem menerima input berupa: jenis aktivitas, kecepatan gerak (m/s), tingkat kepadatan jamaah, suhu lingkungan (°C), kelompok usia, tingkat pengalaman, waktu (siang/malam), dan durasi aktivitas (menit).
**FR-2 — Output Klasifikasi**
Sistem mengeluarkan output klasifikasi 3 kelas risiko: *Low*, *Medium*, dan *High*.
**FR-3 — Probabilitas per Kelas**
Sistem menyertakan probabilitas untuk setiap kelas, bukan hanya label tunggal, agar pembimbing dapat menilai tingkat keyakinan dari prediksi yang dihasilkan.
**FR-4 — Model Re-usable**
Model dapat dipanggil ulang melalui satu fungsi `predict_risk()` tanpa perlu dilakukan retraining setiap kali digunakan.

## 3. Kebutuhan Non-Fungsional

**NFR-1 — Akurasi**
F1-Macro minimal 0.80 pada test set. Target ini telah tercapai, dengan hasil evaluasi menunjukkan ROC-AUC sebesar 0.978 (lihat notebook).
**NFR-2 — Keseimbangan Kelas**
Distribusi `Risk_Level` tidak seimbang, di mana kelas *Low* jauh lebih banyak dibandingkan kelas *High*. Oleh karena itu, model wajib ditangani dengan teknik resampling (SMOTE) agar Recall pada kelas *High* tidak diabaikan.
**NFR-3 — Interoperabilitas**
Model harus dapat di-deploy ulang melalui serialisasi (pickle) tanpa bergantung pada notebook environment tertentu, sehingga dapat dipanggil dari API atau aplikasi lain.
**NFR-4 — Interpretability**
Fitur kontrol seperti `Pilgrim_Group_Size` dan `Phone_Battery_Pct` harus terbukti tidak relevan secara statistik (berdasarkan permutation importance), untuk memastikan model tidak overfit terhadap fitur yang tidak memiliki hubungan kausal dengan risiko.

## 4. Mapping Kebutuhan → Implementasi

**FR-1, FR-2, FR-3, FR-4**
Diimplementasikan pada `main.ipynb`, melalui fungsi `predict_risk()`.
**NFR-1**
Diimplementasikan pada `main.ipynb`, pada bagian evaluasi 5 metrik.
**NFR-2**
Diimplementasikan pada `main.ipynb`, pada blok SMOTE.

**NFR-3**
Diimplementasikan pada `outputs/models/rf_pilgrim_risk.pkl` dan `code/api/main.py`.
**NFR-4**
Diimplementasikan pada `main.ipynb`, pada bagian permutation importance.