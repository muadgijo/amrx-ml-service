"""
Flask API layer for AMR-X inference.
Exposes /predict to return resistance probability.
"""

from flask import Flask, request, jsonify
from model_engine import predict_resistance_amrx

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    """Accept organism and antibiotic names and return resistance probability."""
    data = request.get_json(silent=True) or {}
    organism = data.get("organism")
    antibiotic = data.get("antibiotic")

    if not organism or not antibiotic:
        return jsonify({"error": "organism and antibiotic are required"}), 400

    try:
        prob = predict_resistance_amrx(organism, antibiotic)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({
        "organism": organism,
        "antibiotic": antibiotic,
        "resistance_probability": prob,
    })


if __name__ == "__main__":
    # Development server (not for production)
    app.run(host="0.0.0.0", port=5000, debug=False)
