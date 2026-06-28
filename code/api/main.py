from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(title="Pilgrim Risk Prediction API")

with open("../../outputs/models/rf_pilgrim_risk.pkl", "rb") as f:
    artifact = pickle.load(f)

model = artifact["model"]
le = artifact["label_encoder"]
feature_cols = artifact["feature_cols"]

class RiskInput(BaseModel):
    activity: str
    speed_ms: float
    crowd_density: str
    temperature: float
    age_group: str
    experience: str
    time_of_day: str
    time_spent_min: float
    group_size: int = 20
    battery_pct: int = 80

def build_feature_row(inp: RiskInput):
    sample = {
        "Movement_Speed_ms": inp.speed_ms,
        "Temperature_C": inp.temperature,
        "Time_Spent_min": inp.time_spent_min,
        "Pilgrim_Group_Size": inp.group_size,
        "Phone_Battery_Pct": inp.battery_pct,
    }
    for cat, val in [
        ("Activity_Type", inp.activity),
        ("Crowd_Density", inp.crowd_density),
        ("Pilgrim_Age_Group", inp.age_group),
        ("Pilgrim_Experience", inp.experience),
        ("Time_of_Day", inp.time_of_day),
    ]:
        for col in feature_cols:
            if col.startswith(cat + "_"):
                sample[col] = 1 if col == f"{cat}_{val}" else 0
    return pd.DataFrame([sample])[feature_cols].fillna(0)

@app.post("/predict")
def predict(inp: RiskInput):
    row = build_feature_row(inp)
    pred = model.predict(row)[0]
    proba = model.predict_proba(row)[0]
    return {
        "risk_level": le.inverse_transform([pred])[0],
        "probabilities": dict(zip(le.classes_, proba.round(3).tolist())),
    }

@app.get("/health")
def health():
    return {"status": "ok", "model": "rf_pilgrim_risk", "features": len(feature_cols)}