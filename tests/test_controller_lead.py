from unittest.mock import patch

BASE_LEAD = {"id": 1, "name": "Lucas", "email": "lucas@test.com", "phone": "11999998888"}

# POST /leads/

def test_create_lead_sucesso(client):
    with patch("controllers.lead.create_lead", return_value=BASE_LEAD):
        response = client.post("/leads/", json=BASE_LEAD)
        assert response.status_code == 200
        assert response.json()["email"] == BASE_LEAD["email"]

def test_create_lead_phone_invalido(client):
    payload = {**BASE_LEAD, "phone": "123"}
    response = client.post("/leads/", json=payload)
    assert response.status_code == 422

def test_create_lead_email_invalido(client):
    payload = {**BASE_LEAD, "email": "nao-é-um-email"}
    response = client.post("/leads/", json=payload)
    assert response.status_code == 422

def test_create_lead_duplicado(client):
    with patch("controllers.lead.create_lead", side_effect=ValueError("duplicate")):
        response = client.post("/leads/", json=BASE_LEAD)
        assert response.status_code == 409
        assert "já cadastrado" in response.json()["detail"]

# GET /leads/

def test_get_all_leads(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]) as mock:
        response = client.get("/leads/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        mock.assert_called_once_with(limit=20, offset=0)

def test_get_all_leads_paginacao(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]) as mock:
        response = client.get("/leads/?limit=5&offset=10")
        assert response.status_code == 200
        mock.assert_called_once_with(limit=5, offset=10)

def test_get_leads_filtro_email(client):
    with patch("controllers.lead.get_leads_by_email", return_value=[BASE_LEAD]) as mock:
        response = client.get("/leads/?email=lucas@test.com")
        assert response.status_code == 200
        mock.assert_called_once_with("lucas@test.com")

def test_get_leads_filtro_phone(client):
    with patch("controllers.lead.get_leads_by_phone", return_value=[BASE_LEAD]) as mock:
        response = client.get("/leads/?phone=11999998888")
        assert response.status_code == 200
        mock.assert_called_once_with("11999998888")

# GET /leads/{id}

def test_get_lead_by_id(client):
    with patch("controllers.lead.get_lead_by_id", return_value=[BASE_LEAD]):
        response = client.get("/leads/1")
        assert response.status_code == 200

def test_get_lead_id_nao_numerico(client):
    response = client.get("/leads/abc")
    assert response.status_code == 422

def test_get_lead_by_id_nao_encontrado(client):
    with patch("controllers.lead.get_lead_by_id", return_value=[]):
        response = client.get("/leads/999")
        assert response.status_code == 404

def test_get_leads_email_nao_encontrado(client):
    with patch("controllers.lead.get_leads_by_email", return_value=[]):
        response = client.get("/leads/?email=naoexiste@test.com")
        assert response.status_code == 404

def test_get_leads_phone_nao_encontrado(client):
    with patch("controllers.lead.get_leads_by_phone", return_value=[]):
        response = client.get("/leads/?phone=11999990000")
        assert response.status_code == 404



