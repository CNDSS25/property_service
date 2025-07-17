from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """
    Testet, ob der Root-Endpunkt des Services erreichbar ist.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Product Service is running"}