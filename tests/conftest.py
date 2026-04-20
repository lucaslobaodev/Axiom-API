import pytest
from fastapi.testclient import TestClient
from main import app
from core.config import settings

@pytest.fixture
def client():
    return TestClient(app, headers={"X-API-Key": settings.API_KEY})
