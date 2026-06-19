from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_readyz():
    response = client.get("/readyz")

    assert response.status_code in [200, 503]