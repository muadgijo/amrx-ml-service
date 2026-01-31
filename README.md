# AMR-X ML Service

REST API for antimicrobial resistance prediction using XGBoost.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Server runs at http://localhost:5000
```

### Test API

```bash
# Health check
curl http://localhost:5000/

# Get model info
curl http://localhost:5000/api/v1/info

# Make prediction
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
```

## 📡 API Endpoints

### 1. Health Check
```
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "service": "AMR-X ML API",
  "version": "v1",
  "model": "xgboost_v1.0"
}
```

---

### 2. Model Info
```
GET /api/v1/info
```

**Response:**
```json
{
  "model_name": "xgboost_v1.0",
  "trained_on": "ARMD (Global Antimicrobial Resistance Dataset)",
  "last_updated": "2025-01-15",
  "disclaimer": "Decision-support only. Not for clinical diagnosis."
}
```

---

### 3. Predict Resistance
```
POST /api/v1/predict
Content-Type: application/json
```

**Request:**
```json
{
  "organism": "ESCHERICHIA COLI",
  "antibiotic": "Ciprofloxacin"
}
```

**Response:**
```json
{
  "probability": 0.498,
  "percentage": "49.8%",
  "risk_level": "moderate-low",
  "organism": "ESCHERICHIA COLI",
  "antibiotic": "Ciprofloxacin",
  "model_version": "xgboost_v1.0",
  "timestamp": "2025-01-29T12:34:56Z"
}
```

**Risk Levels:**
- `low`: < 30% resistance probability
- `moderate-low`: 30-50%
- `moderate-high`: 50-70%
- `high`: > 70%

---

## ✅ Valid Inputs

### Organisms (case-sensitive, UPPERCASE)
See `organism_map.csv` for complete list. Examples:
- `ESCHERICHIA COLI`
- `STAPHYLOCOCCUS AUREUS`
- `PSEUDOMONAS AERUGINOSA`

### Antibiotics (case-sensitive)
See `antibiotic_map.csv` for complete list. Examples:
- `Ciprofloxacin`
- `Amikacin`
- `Vancomycin`

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing
```

---

## 🚀 Deployment

Deployed on **Render** at: `https://amrx-ml-api.onrender.com`

Auto-deploys on push to `main` branch via GitHub Actions.

---

## 🔒 Rate Limits

- **Default:** 100 requests per hour per IP
- **Predict endpoint:** 30 requests per minute per IP

---

## 📧 For Teammates

**API Base URL:** `https://amrx-ml-api.onrender.com`

**Example Integration (JavaScript):**
```javascript
fetch('https://amrx-ml-api.onrender.com/api/v1/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    organism: 'ESCHERICHIA COLI',
    antibiotic: 'Ciprofloxacin'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## ⚠️ Disclaimer

This is a **decision-support tool for educational purposes**. Not for clinical use.

---

## 📝 License

College project - educational use only.

