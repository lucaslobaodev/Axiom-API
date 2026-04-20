from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_ok():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=MagicMock())
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    with patch("controllers.health.get_connection", return_value=mock_conn):
        with patch("controllers.health.release_connection"):
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

def test_health_banco_fora():
    with patch("controllers.health.get_connection", side_effect=Exception("connection refused")):
        response = client.get("/health")
        assert response.status_code == 503
