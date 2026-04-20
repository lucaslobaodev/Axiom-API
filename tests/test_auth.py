from fastapi.testclient import TestClient
from main import app

client_sem_key = TestClient(app, raise_server_exceptions=False)

def test_sem_api_key_retorna_401():
    response = client_sem_key.post("/leads/", json={})
    assert response.status_code == 401

def test_key_invalida_retorna_403():
    response = client_sem_key.post("/leads/", json={}, headers={"X-API-Key": "key-errada"})
    assert response.status_code == 403
