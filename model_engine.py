"""
AMR-X Model Engine

Core ML logic for antimicrobial resistance prediction.
Loads the XGBoost model and mapping CSVs once on import.
"""

import pandas as pd
import xgboost as xgb

# Keep XGBoost quiet during import/prediction
xgb.set_config(verbosity=0)

# Load the model once (global, on module import)
model = xgb.Booster()
model.load_model("amr_model.json")

# Load the mappings (organism and antibiotic code lookups)
organism_map = pd.read_csv("organism_map.csv")
antibiotic_map = pd.read_csv("antibiotic_map.csv")

# Create lookup dictionaries for fast name→code conversion
organism_lookup = dict(zip(organism_map["organism"], organism_map["organism_code"]))
antibiotic_lookup = dict(zip(antibiotic_map["antibiotic"], antibiotic_map["antibiotic_code"]))


def predict_resistance_amrx(organism: str, antibiotic: str) -> float:
    """
    Predict the probability that an organism is resistant to an antibiotic.
    
    Args:
        organism (str): Name of the organism (e.g., "E.COLI")
        antibiotic (str): Name of the antibiotic (e.g., "Amoxicillin/Clavulanic Acid")
    
    Returns:
        float: Probability of resistance (0.0 to 1.0)
    
    Raises:
        ValueError: If organism or antibiotic is not found in the mappings
    """
    
    # Look up the numeric codes
    if organism not in organism_lookup:
        raise ValueError(f"Unknown organism: {organism}")
    if antibiotic not in antibiotic_lookup:
        raise ValueError(f"Unknown antibiotic: {antibiotic}")
    
    organism_code = organism_lookup[organism]
    antibiotic_code = antibiotic_lookup[antibiotic]
    
    # Create feature matrix with explicit column names expected by the model
    features = [[organism_code, antibiotic_code]]
    dmatrix = xgb.DMatrix(features, feature_names=["organism_code", "antibiotic_code"])

    # Predict using the model
    prediction = model.predict(dmatrix)
    
    # Return probability (first element of prediction array)
    return float(prediction[0])
