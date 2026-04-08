import pytest
import httpx
from main import app

@pytest.mark.asyncio
async def test_health_check():
    """Verify service health endpoint."""
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_analyze_endpoint_success():
    """Verify successful NLP analysis with multi-model async logic."""
    payload = {"text": "Sundar Pichai is the CEO of Google in Mountain View."}
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert "tokens" in data
    assert "Sundar Pichai" in data["entities"]["Person"]
    assert "Google" in data["entities"]["Organisation"]
    assert "Mountain View" in data["entities"]["Location"]
    assert data["detected_language"] == "en"

@pytest.mark.asyncio
async def test_analyze_endpoint_blank_text():
    """Verify validation for blank but non-empty strings (Pydantic validator)."""
    payload = {"text": "   "}
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/analyze", json=payload)
    
    assert response.status_code == 422 # Standard Unprocessable Entity for Pydantic validation error

@pytest.mark.asyncio
async def test_analyze_endpoint_too_long_payload():
    """Verify strict length constraints (50KB cap)."""
    # 51KB string
    payload = {"text": "a" * 51000}
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/analyze", json=payload)
    
    assert response.status_code == 422
    assert "50000" in str(response.json())

@pytest.mark.asyncio
async def test_analyze_endpoint_missing_field():
    """Verify schema enforcement for missing 'text' field."""
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/analyze", json={})
    assert response.status_code == 422
