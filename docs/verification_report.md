# Verification Report — Pilgrim Risk Prediction System

## Ringkasan Verifikasi Kebutuhan

**FR-1 — Input 8 Parameter Aktivitas**
Diimplementasikan melalui `RiskInput` schema pada `code/api/main.py`.
**FR-2 — Output 3 Kelas Risiko**
Diimplementasikan melalui endpoint `/predict`.
**FR-3 — Probabilitas per Kelas**
Diimplementasikan melalui field `probabilities` pada response API.
Contoh output:
- Low: 0.12
- Medium: 0.31
- High: 0.57
**FR-4 — Re-usable Tanpa Retraining**
Model dimuat sekali saat startup API (`pickle.load`), kemudian dipanggil berulang kali melalui endpoint tanpa perlu dilatih ulang.
**NFR-1 — F1-Macro ≥ 0.80**
Berdasarkan hasil evaluasi pada `main.ipynb`.
**NFR-3 — Interoperabilitas Lintas Platform**
Diuji melalui demo API dan Web (`code/web/app.py`). Pengujian manual menunjukkan input yang sama pada web menghasilkan output yang identik dengan fungsi `predict_risk()` di notebook.
---

## Catatan Pengujian Manual

Pengujian dilakukan dengan **3 skenario kasus uji**, yaitu jamaah dengan tingkat risiko *tinggi*, *sedang*, dan *rendah*. Prosedurnya sebagai berikut:

1. Input dikirim ke endpoint `/predict` melalui web demo.
2. Hasil prediksi dicocokkan dengan output fungsi `predict_risk()` pada notebook asli.
3. Kedua hasil dibandingkan untuk memastikan konsistensi.

**Hasil:** Output identik pada seluruh skenario pengujian, sehingga mengonfirmasi konsistensi model antar platform (API dan Web).