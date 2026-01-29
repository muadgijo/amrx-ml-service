import xgboost as xgb
import pandas as pd
import numpy as np

# Load everything ONCE
model = xgb.Booster()
model.load_model("amr_model.json")

organism_map = pd.read_csv("organism_map.csv")
antibiotic_map = pd.read_csv("antibiotic_map.csv")

THRESHOLD = 0.476


def predict_resistance_amrx(organism, antibiotic):
    # Convert organism name → code
    org_row = organism_map[organism_map["organism"] == organism]
    if org_row.empty:
        return {"error": "Unknown organism"}

    abx_row = antibiotic_map[antibiotic_map["antibiotic"] == antibiotic]
    if abx_row.empty:
        return {"error": "Unknown antibiotic"}

    org_code = org_row["organism_code"].values[0]
    abx_code = abx_row["antibiotic_code"].values[0]

    X = np.array([[org_code, abx_code]])
    dtest = xgb.DMatrix(
        X,
        feature_names=["organism_code", "antibiotic_code"]
    )

    prob = float(model.predict(dtest)[0])
    label = "Resistant" if prob >= THRESHOLD else "Susceptible"

    return {
        "organism": organism,
        "antibiotic": antibiotic,
        "probability": round(prob, 3),
        "prediction": label
    }
