from flask import Flask, request, jsonify
from flask_cors import CORS
from model_engine import predict_resistance_amrx
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "AMR-X API"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or {}
        organism = data.get("organism", "").strip()
        antibiotic = data.get("antibiotic", "").strip()

        if not organism or not antibiotic:
            return jsonify({"error": "organism and antibiotic required"}), 400

        prob = predict_resistance_amrx(organism, antibiotic)
        
        return jsonify({
            "probability": round(prob, 3),
            "percentage": f"{prob * 100:.1f}%",
            "organism": organism,
            "antibiotic": antibiotic
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
