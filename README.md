# AMR-X ML Service

Simple API that predicts if bacteria resist antibiotics.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server runs at `http://localhost:5000`

## Usage

**Health check:**
```bash
curl http://localhost:5000/
```

**Predict:**
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"organism\":\"ESCHERICHIA COLI\",\"antibiotic\":\"Ciprofloxacin\"}"
```

**Response:**
```json
{
  "probability": 0.498,
  "percentage": "49.8%",
  "organism": "ESCHERICHIA COLI",
  "antibiotic": "Ciprofloxacin"
}
```

## Valid Inputs

- **Organisms:** See `organism_map.csv` (309 bacteria, UPPERCASE)
- **Antibiotics:** See `antibiotic_map.csv` (50 antibiotics, case-sensitive)

Examples:
- `ESCHERICHIA COLI` + `Ciprofloxacin`
- `STAPHYLOCOCCUS AUREUS` + `Vancomycin`

## Files

- `app.py` - Flask API
- `model_engine.py` - ML prediction logic  
- `test_predict.py` - Test script
- `amr_model.json` - XGBoost model
- `organism_map.csv` - Bacteria names
- `antibiotic_map.csv` - Antibiotic names

## Test

```bash
python test_predict.py
```

## If you see import errors (quick fix)

```bash
pip install --force-reinstall --no-cache-dir -r requirements.txt
```

That's it!
