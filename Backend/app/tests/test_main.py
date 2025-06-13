from fastapi.testclient import TestClient
from Backend.app.main import app  # import your FastAPI app

client = TestClient(app)

def test_shorten_url():
    response = client.post("/shortyfy", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http")

def test_redirect_url_not_found():
    response = client.get("/nonexistentid")
    assert response.status_code == 404