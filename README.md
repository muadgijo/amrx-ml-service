AMR-X ML Inference Service
Overview

This repository contains the AMR-X machine learning inference service.

It packages a pre-trained XGBoost model and exposes it through a Flask REST API for predicting the likelihood that a given organism is resistant to a given antibiotic.

This service is:

Inference-only (no training, no online learning)

Backend-agnostic (can be called from any system over HTTP)

Designed as a standalone ML microservice for integration with the AMR-X platform

The model is frozen and all predictions are deterministic based on the packaged artifacts.

What This Service Does
Input

Organism name (string)

Antibiotic name (string)

Process

Maps names to numeric codes using fixed CSV mappings

Feeds the encoded pair into a pre-trained XGBoost model

Returns a resistance probability between 0.0 and 1.0

Output

Raw resistance probability (no thresholding applied)

Architecture

HTTP Client (frontend / backend / Postman / curl)
→ POST /predict (JSON)
→ Flask API (app.py)
→ Model Engine (model_engine.py)
→ XGBoost model + CSV mappings

The model and mappings are loaded once at startup and kept in memory.

Repository Structure

app.py — Flask API entrypoint
model_engine.py — Core ML inference engine
test_predict.py — Manual sanity tests
amr_model.json — Frozen trained XGBoost model
organism_map.csv — Organism → code mapping
antibiotic_map.csv — Antibiotic → code mapping
requirements.txt — Python dependencies
legacy/ — Deprecated scripts
.gitignore — Git ignore rules

Installation
1. Clone the repository

git clone https://github.com/muadgijo/amrx-ml-service.git

cd amrx-ml-service

2. Create and activate a virtual environment

Windows (PowerShell):

python -m venv .venv
.venv\Scripts\Activate.ps1

Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

Running Manual Tests

python test_predict.py

This runs a few hard-coded organism/antibiotic pairs and prints predicted probabilities.

Running the API

python app.py

The service will start on:

http://127.0.0.1:5000

API Contract
Endpoint

POST /predict

Request Body (JSON)

{
"organism": "ESCHERICHIA COLI",
"antibiotic": "Ciprofloxacin"
}

Notes:

Values must match entries in the CSV mapping files

Matching is currently case-sensitive

Successful Response (200)

{
"organism": "ESCHERICHIA COLI",
"antibiotic": "Ciprofloxacin",
"resistance_probability": 0.498005747795105
}

resistance_probability is a float between 0.0 and 1.0.

Error Responses

Missing fields (400):

{ "error": "organism and antibiotic are required" }

Unknown organism or antibiotic (400):

{ "error": "Unknown organism: <name>" }

Internal error (500):

{ "error": "Something went wrong" }

Quick Test Call

PowerShell:

Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict
" -Method Post -ContentType "application/json" -Body '{"organism":"ESCHERICHIA COLI","antibiotic":"Ciprofloxacin"}'

curl:

curl -X POST http://127.0.0.1:5000/predict
 -H "Content-Type: application/json" -d '{"organism":"ESCHERICHIA COLI","antibiotic":"Ciprofloxacin"}'

Design Constraints

No retraining in this service

No live clinical data

No hospital integration

Static artifacts only (model + mappings)

Intended for academic and analytical use

Ownership

This repository represents the ML subsystem of the AMR-X platform.

It is designed to be consumed as a black-box prediction service by backend systems, analytics pipelines, and dashboards.
