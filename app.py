from flask import Flask, request, jsonify
from flask_cors import CORS
from model_engine import predict_resistance_amrx
import logging

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}

        organism = data.get("organism")
        antibiotic = data.get("antibiotic")

        if not organism or not antibiotic:
            logging.warning("Missing organism or antibiotic in request")
            return jsonify({"error": "organism and antibiotic are required"}), 400

        logging.info(
            "Request received | organism=%s, antibiotic=%s", organism, antibiotic
        )

        result = predict_resistance_amrx(organism, antibiotic)

        logging.info(
            "Prediction completed | organism=%s, antibiotic=%s, result=%s",
            organism,
            antibiotic,
            result,
        )

        return jsonify(result)

    except Exception:
        logging.exception("Unexpected error during prediction")
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
