"""
AMR-X Model Engine
Loads model and predicts resistance probability.
"""

import pandas as pd
import xgboost as xgb

xgb.set_config(verbosity=0)

# Load model and data
model = xgb.Booster()
model.load_model("amr_model.json")
organism_map = pd.read_csv("organism_map.csv")
antibiotic_map = pd.read_csv("antibiotic_map.csv")

organism_lookup = dict(zip(organism_map["organism"], organism_map["organism_code"]))
antibiotic_lookup = dict(zip(antibiotic_map["antibiotic"], antibiotic_map["antibiotic_code"]))


def predict_resistance_amrx(organism: str, antibiotic: str) -> float:
    """Predict resistance probability (0.0 to 1.0)"""
    
    if organism not in organism_lookup:
        raise ValueError(f"Unknown organism: {organism}")
    if antibiotic not in antibiotic_lookup:
        raise ValueError(f"Unknown antibiotic: {antibiotic}")
    
    org_code = organism_lookup[organism]
    abx_code = antibiotic_lookup[antibiotic]
    
    features = [[org_code, abx_code]]
    dmatrix = xgb.DMatrix(features, feature_names=["organism_code", "antibiotic_code"])
    prediction = model.predict(dmatrix)
    
    return float(prediction[0])
