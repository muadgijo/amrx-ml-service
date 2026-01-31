# Test Cases for AMR-X ML API

## Setup
Start the server first:
```bash
python app.py
```

Server runs at: `http://localhost:5000`

---

## 1. HEALTH CHECK

### Test 1.1: Server is running
```bash
curl http://localhost:5000/
```

**Expected Response (200):**
```json
{
  "status": "healthy",
  "service": "AMR-X ML API",
  "version": "v1",
  "model": "xgboost_v1.0"
}
```

---

## 2. MODEL INFO

### Test 2.1: Get model information
```bash
curl http://localhost:5000/api/v1/info
```

**Expected Response (200):**
```json
{
  "model_name": "xgboost_v1.0",
  "trained_on": "ARMD (Global Antimicrobial Resistance Dataset)",
  "last_updated": "2025-01-15",
  "disclaimer": "Decision-support only. Not for clinical diagnosis."
}
```

---

## 3. VALID PREDICTIONS

### Test 3.1: E. coli + Ciprofloxacin
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
```

**Expected Response (200):**
```json
{
  "probability": 0.498,
  "percentage": "49.8%",
  "risk_level": "moderate-low",
  "organism": "ESCHERICHIA COLI",
  "antibiotic": "Ciprofloxacin",
  "model_version": "xgboost_v1.0",
  "timestamp": "2026-01-31T20:45:12.345678Z"
}
```

### Test 3.2: S. aureus + Vancomycin
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "STAPHYLOCOCCUS AUREUS", "antibiotic": "Vancomycin"}'
```

**Expected Response (200):** probability + risk_level

### Test 3.3: P. aeruginosa + Cefepime
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "PSEUDOMONAS AERUGINOSA", "antibiotic": "Cefepime"}'
```

**Expected Response (200):** probability + risk_level

---

## 4. ERROR HANDLING - Missing Fields

### Test 4.1: Missing organism
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"antibiotic": "Ciprofloxacin"}'
```

**Expected Response (400):**
```json
{
  "error": "Missing required field: organism"
}
```

### Test 4.2: Missing antibiotic
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI"}'
```

**Expected Response (400):**
```json
{
  "error": "Missing required field: antibiotic"
}
```

### Test 4.3: Empty JSON body
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response (400):**
```json
{
  "error": "Missing required field: organism"
}
```

### Test 4.4: No JSON body
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json"
```

**Expected Response (400):**
```json
{
  "error": "Request body is empty"
}
```

---

## 5. ERROR HANDLING - Invalid Inputs

### Test 5.1: Invalid organism
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "FAKE_ORGANISM", "antibiotic": "Ciprofloxacin"}'
```

**Expected Response (400):**
```json
{
  "error": "Unknown organism: FAKE_ORGANISM",
  "hint": "Check organism_map.csv and antibiotic_map.csv for valid inputs"
}
```

### Test 5.2: Invalid antibiotic
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "FAKE_DRUG"}'
```

**Expected Response (400):**
```json
{
  "error": "Unknown antibiotic: FAKE_DRUG",
  "hint": "Check organism_map.csv and antibiotic_map.csv for valid inputs"
}
```

### Test 5.3: Case sensitivity - organism
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "escherichia coli", "antibiotic": "Ciprofloxacin"}'
```

**Expected Response (400):** (organism must be UPPERCASE)
```json
{
  "error": "Unknown organism: escherichia coli"
}
```

---

## 6. WHITESPACE HANDLING

### Test 6.1: Leading/trailing spaces
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "  ESCHERICHIA COLI  ", "antibiotic": "  Ciprofloxacin  "}'
```

**Expected Response (200):** Should work (spaces are trimmed)

---

## 7. INVALID ROUTES

### Test 7.1: Non-existent endpoint
```bash
curl http://localhost:5000/invalid-endpoint
```

**Expected Response (404):**
```json
{
  "error": "Endpoint not found"
}
```

### Test 7.2: Wrong HTTP method
```bash
curl -X DELETE http://localhost:5000/
```

**Expected Response (405):** Method not allowed

---

## 8. RATE LIMITING

### Test 8.1: Exceed 30 requests per minute
Make 31+ rapid requests to `/api/v1/predict`:

```bash
for i in {1..35}; do
  curl -X POST http://localhost:5000/api/v1/predict \
    -H "Content-Type: application/json" \
    -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
done
```

**Expected Response:** First 30 return (200), requests 31+ return (429)
```json
{
  "error": "Too many requests. Max 30 per minute."
}
```

---

## 9. RESPONSE VALIDATION

### Test 9.1: Response has all required fields
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
```

Check response contains:
- ✅ `probability` (float, 0-1)
- ✅ `percentage` (string with %)
- ✅ `risk_level` (string: low/moderate-low/moderate-high/high)
- ✅ `organism` (string)
- ✅ `antibiotic` (string)
- ✅ `model_version` (string)
- ✅ `timestamp` (string ending with Z)

---

## 10. CONSISTENCY TEST

### Test 10.1: Same input produces same output
```bash
# Request 1
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'

# Request 2 (same input)
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"organism": "ESCHERICHIA COLI", "antibiotic": "Ciprofloxacin"}'
```

**Expected:** Both responses have same probability value

---

## Summary

**Total Tests: 24**
- Health & Info: 2
- Valid Predictions: 3
- Missing Fields: 4
- Invalid Inputs: 3
- Whitespace: 1
- Invalid Routes: 2
- Rate Limiting: 1
- Response Validation: 1
- Consistency: 1

**If all pass → API is production-ready! ✅**
