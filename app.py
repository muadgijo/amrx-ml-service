"""
AMR-X ML Service API
Simple REST API for antimicrobial resistance prediction.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime
from collections import defaultdict
from time import time

from model_engine import predict_resistance_amrx

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Simple rate limiting (in-memory)
request_history = defaultdict(list)

def check_rate_limit(ip: str, limit: int = 30, window: int = 60) -> bool:
    """Simple rate limiter (30 req/min per IP)."""
    now = time()
    request_history[ip] = [t for t in request_history[ip] if now - t < window]
    if len(request_history[ip]) >= limit:
        return False
    request_history[ip].append(now)
    return True

# Model info
MODEL_INFO = {
    "model_name": "xgboost_v1.0",
    "trained_on": "ARMD (Global Antimicrobial Resistance Dataset)",
    "last_updated": "2025-01-15",
    "disclaimer": "Decision-support only. Not for clinical diagnosis."
}

API_VERSION = "v1"


def get_risk_level(probability: float) -> str:
    """Convert probability to risk level."""
    if probability < 0.3:
        return "low"
    elif probability < 0.5:
        return "moderate-low"
    elif probability < 0.7:
        return "moderate-high"
    else:
        return "high"


@app.route("/", methods=["GET"])
def health():
    """Health check - verify API is running."""
    return jsonify({
        "status": "healthy",
        "service": "AMR-X ML API",
        "version": API_VERSION,
        "model": MODEL_INFO["model_name"]
    }), 200


@app.route(f"/api/{API_VERSION}/info", methods=["GET"])
def info():
    """Get model information."""
    logger.info("Model info requested")
    return jsonify(MODEL_INFO), 200


@app.route(f"/api/{API_VERSION}/predict", methods=["POST"])
def predict():
    """
    Predict antimicrobial resistance.
    
    Request (JSON):
        {"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}
    
    Response (JSON):
        {"probability": 0.498, "percentage": "49.8%", "risk_level": "moderate-low", ...}
    """
    try:
        # Get client IP
        ip = request.remote_addr or "unknown"
        
        # Check rate limit
        if not check_rate_limit(ip):
            logger.warning(f"Rate limit exceeded from {ip}")
            return jsonify({"error": "Too many requests. Max 30 per minute."}), 429
        
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({"error": "Request body is empty"}), 400
        
        organism = data.get("organism", "").strip()
        antibiotic = data.get("antibiotic", "").strip()
        
        if not organism or not antibiotic:
            missing = "organism" if not organism else "antibiotic"
            return jsonify({"error": f"Missing required field: {missing}"}), 400
        
        logger.info(f"Prediction request | {organism} vs {antibiotic}")
        
        probability = predict_resistance_amrx(organism, antibiotic)
        risk_level = get_risk_level(probability)
        
        result = {
            "probability": round(probability, 4),
            "percentage": f"{probability * 100:.1f}%",
            "risk_level": risk_level,
            "organism": organism,
            "antibiotic": antibiotic,
            "model_version": MODEL_INFO["model_name"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        logger.info(f"Success | {organism} vs {antibiotic} = {probability:.3f} ({risk_level})")
        
        return jsonify(result), 200
    
    except ValueError as e:
        error_msg = str(e)
        logger.warning(f"Validation error: {error_msg}")
        return jsonify({
            "error": error_msg,
            "hint": "Check organism_map.csv and antibiotic_map.csv for valid inputs"
        }), 400
    
    except Exception as e:
        logger.exception("Unexpected error during prediction")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting AMR-X ML API {API_VERSION}")
    logger.info(f"Model: {MODEL_INFO['model_name']}")
    app.run(host="0.0.0.0", port=port, debug=False)
