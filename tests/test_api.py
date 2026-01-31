"""
Simple tests for AMR-X API.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health endpoint works."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_model_info(client):
    """Test model info endpoint."""
    response = client.get('/api/v1/info')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'model_name' in data


def test_predict_success(client):
    """Test successful prediction."""
    payload = {
        "organism": "ESCHERICHIA COLI",
        "antibiotic": "Ciprofloxacin"
    }
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'probability' in data
    assert 'risk_level' in data
    assert 0 <= data['probability'] <= 1


def test_predict_missing_organism(client):
    """Test fails without organism."""
    payload = {"antibiotic": "Ciprofloxacin"}
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_predict_invalid_organism(client):
    """Test fails with invalid organism."""
    payload = {
        "organism": "FAKE_ORGANISM",
        "antibiotic": "Ciprofloxacin"
    }
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 400
