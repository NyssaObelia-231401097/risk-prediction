# Verification Report — Pilgrim Risk Prediction System

| ID Kebutuhan | Deskripsi | Implementasi | Status Verifikasi |
|---|---|---|---|
| FR-1 | Input 8 parameter aktivitas | `RiskInput` schema, `code/api/main.py` | ✅ Terpenuhi |
| FR-2 | Output 3 kelas | endpoint `/predict` | ✅ Terpenuhi |
| FR-3 | Probabilitas per kelas | Field `probabilities` pada response API | ✅ Terpenuhi, contoh: Low 0.12, Medium 0.31, High 0.57 |
| FR-4 | Re-usable tanpa retraining | Model dimuat sekali di startup API (`pickle.load`), dipanggil berulang lewat endpoint | ✅ Terpenuhi |
| NFR-1 | F1-Macro ≥ 0.80 | Hasil evaluasi `main.ipynb` | ✅ Terpenuhi |
| NFR-3 | Interoperabilitas lintas platform | Demo API + Web (`code/web/app.py`) | ✅ Terpenuhi, diuji manual: input sama di web menghasilkan output identik dengan `predict_risk()` di notebook |

## Catatan Pengujian Manual
Pengujian dilakukan dengan 3 skenario kasus uji (jamaah berisiko tinggi,
sedang, rendah) yang dikirim ke endpoint `/predict` lewat web demo dan
dicocokkan hasilnya dengan prediksi `predict_risk()` di notebook asli —
hasil identik, mengonfirmasi konsistensi model antar platform.