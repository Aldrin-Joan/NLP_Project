import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_analyze_endpoint_success(client):
    payload = {"text": "Bill Gates founded Microsoft in Seattle."}
    rv = client.post('/analyze', 
                     data=json.dumps(payload),
                     content_type='application/json')
    
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert "entities" in data
    assert "tokens" in data
    assert "Bill Gates" in data["entities"]["Person"]
    assert "Microsoft" in data["entities"]["Organisation"]

def test_analyze_endpoint_empty_text(client):
    payload = {"text": ""}
    rv = client.post('/analyze', 
                     data=json.dumps(payload),
                     content_type='application/json')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert all(len(v) == 0 for v in data["entities"].values())

def test_analyze_endpoint_missing_field(client):
    rv = client.post('/analyze', 
                     data=json.dumps({}),
                     content_type='application/json')
    assert rv.status_code == 400

def test_analyze_endpoint_too_long(client):
    payload = {"text": "a" * 10001}
    rv = client.post('/analyze', 
                     data=json.dumps(payload),
                     content_type='application/json')
    assert rv.status_code == 413
