# AMR-X: Antimicrobial Resistance Prediction Service

A simple ML inference service that predicts antibiotic resistance probability for organism-antibiotic pairs using a trained XGBoost model.

## Project Overview

- **Purpose:** College ML project - inference only (no retraining)
- **Input:** Organism name + Antibiotic name
- **Output:** Resistance probability (0.0 to 1.0)
- **Backend-agnostic:** HTTP REST API callable from any client

## Architecture

```
HTTP Client → Flask API (app.py) → Model Engine (model_engine.py) → XGBoost Model
```

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/muadgijo/amrx-ml-service.git
cd amrx-ml-service
```

2. **Create and activate virtual environment**
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Run Manual Tests

```bash
python test_predict.py
```

**Output:**
```
Manual AMR-X predictions

ESCHERICHIA COLI vs Ciprofloxacin -> resistance probability: 0.498
ACINETOBACTER BAUMANNII vs Amikacin -> resistance probability: 0.774
STAPHYLOCOCCUS AUREUS vs Vancomycin -> resistance probability: 0.106
PSEUDOMONAS AERUGINOSA vs Cefepime -> resistance probability: 0.304
```

### Start the Flask API

```bash
python app.py
```

Server starts on `http://0.0.0.0:5000`

### Call the API

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
```

**curl:**
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
```

**Python:**
```python
import requests
response = requests.post('http://127.0.0.1:5000/predict', json={
    'organism': 'ESCHERICHIA COLI',
    'antibiotic': 'Ciprofloxacin'
})
print(response.json())
```

## API Reference

### POST /predict

**Request:**
```json
{
  "organism": "ESCHERICHIA COLI",
  "antibiotic": "Ciprofloxacin"
}
```

**Success Response (200):**
```json
0.498005747795105
```

**Error Response (400):**
```json
{
  "error": "organism and antibiotic are required"
}
```

**Error Response (500):**
```json
{
  "error": "Something went wrong"
}
```

## Valid Inputs

### Organisms (case-sensitive, examples)
- `ESCHERICHIA COLI`
- `ACINETOBACTER BAUMANNII`
- `STAPHYLOCOCCUS AUREUS`
- `PSEUDOMONAS AERUGINOSA`
- See `organism_map.csv` for full list (300+ organisms)

### Antibiotics (case-sensitive, examples)
- `Ciprofloxacin`
- `Amikacin`
- `Vancomycin`
- `Cefepime`
- `Amoxicillin/Clavulanic Acid`
- See `antibiotic_map.csv` for full list (50 antibiotics)

## Project Structure

```
amrx-ml-service/
├── app.py                   # Flask API with logging
├── model_engine.py          # ML core (loads model + CSVs)
├── test_predict.py          # Manual test script
├── amr_model.json           # Trained XGBoost model
├── organism_map.csv         # Organism name → code mapping
├── antibiotic_map.csv       # Antibiotic name → code mapping
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
└── legacy/                  # Old/unused files
    ├── ml_api.py            # Previous API version
    └── predict.py           # Previous prediction logic
```

## Dependencies

- Python 3.10+
- Flask 3.1.2
- XGBoost 3.1.3
- Pandas 2.3.3
- NumPy 2.4.1

## Notes

- **No retraining:** Model is frozen (inference only)
- **No live data:** Static CSV mappings
- **Development only:** Not for production deployment
- **CORS enabled:** Safe for frontend integration

## License

College project - educational use only
