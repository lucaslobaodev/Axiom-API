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

def test_create_lead_duplicado_retorna_lead_existente(client):
    with patch("controllers.lead.create_lead", return_value=BASE_LEAD):
        response = client.post("/leads/", json=BASE_LEAD)
        assert response.status_code == 200
        assert response.json()["email"] == BASE_LEAD["email"]

# GET /leads/

def test_get_all_leads(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]), \
         patch("controllers.lead.count_all_leads", return_value=1):
        response = client.get("/leads/")
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        assert body["limit"] == 20
        assert body["offset"] == 0
        assert body["data"][0]["email"] == BASE_LEAD["email"]

def test_get_all_leads_paginacao(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]), \
         patch("controllers.lead.count_all_leads", return_value=1):
        response = client.get("/leads/?limit=5&offset=10")
        assert response.status_code == 200
        body = response.json()
        assert body["limit"] == 5
        assert body["offset"] == 10

def test_get_all_leads_ordenado_por_name(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]) as mock, \
         patch("controllers.lead.count_all_leads", return_value=1):
        response = client.get("/leads/?order_by=name&direction=desc")
        assert response.status_code == 200
        mock.assert_called_once_with(limit=20, offset=0, order_by="name", direction="desc", phone_contains=None)

def test_get_all_leads_order_by_invalido(client):
    response = client.get("/leads/?order_by=senha")
    assert response.status_code == 422

def test_get_all_leads_direction_invalida(client):
    response = client.get("/leads/?direction=lateral")
    assert response.status_code == 422

def test_get_all_leads_phone_contains(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]) as mock, \
         patch("controllers.lead.count_all_leads", return_value=1):
        response = client.get("/leads/?phone_contains=%2B5561")
        assert response.status_code == 200
        mock.assert_called_once_with(limit=20, offset=0, order_by="id", direction="asc", phone_contains="+5561")

def test_get_leads_filtro_email(client):
    with patch("controllers.lead.get_leads_by_email", return_value=[BASE_LEAD]):
        response = client.get("/leads/?email=lucas@test.com")
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        assert body["data"][0]["email"] == BASE_LEAD["email"]

def test_get_leads_filtro_phone(client):
    with patch("controllers.lead.get_leads_by_phone", return_value=[BASE_LEAD]):
        response = client.get("/leads/?phone=11999998888")
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        assert body["data"][0]["phone"] == BASE_LEAD["phone"]

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

# Query param validation: limit e offset

def test_limit_zero_retorna_422(client):
    response = client.get("/leads/?limit=0")
    assert response.status_code == 422

def test_limit_negativo_retorna_422(client):
    response = client.get("/leads/?limit=-1")
    assert response.status_code == 422

def test_limit_acima_do_maximo_retorna_422(client):
    response = client.get("/leads/?limit=1001")
    assert response.status_code == 422

def test_offset_negativo_retorna_422(client):
    response = client.get("/leads/?offset=-1")
    assert response.status_code == 422

def test_limit_no_maximo_aceito(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]) as mock:
        response = client.get("/leads/?limit=1000")
        assert response.status_code == 200
        mock.assert_called_once_with(limit=1000, offset=0, order_by="id", direction="asc", phone_contains=None)

def test_limit_no_minimo_aceito(client):
    with patch("controllers.lead.get_all_leads", return_value=[BASE_LEAD]) as mock:
        response = client.get("/leads/?limit=1")
        assert response.status_code == 200
        mock.assert_called_once_with(limit=1, offset=0, order_by="id", direction="asc", phone_contains=None)

# DELETE /leads/{id}

def test_delete_lead_sucesso(client):
    with patch("controllers.lead.soft_delete_lead", return_value=[{"id": 1}]):
        response = client.delete("/leads/1")
        assert response.status_code == 204

def test_delete_lead_nao_encontrado(client):
    with patch("controllers.lead.soft_delete_lead", return_value=[]):
        response = client.delete("/leads/999")
        assert response.status_code == 404

def test_delete_lead_id_nao_numerico(client):
    response = client.delete("/leads/abc")
    assert response.status_code == 422

def test_delete_lead_ja_deletado_retorna_404(client):
    # soft_delete retorna [] quando deleted_at já estava preenchido (RETURNING não devolve nada)
    with patch("controllers.lead.soft_delete_lead", return_value=[]):
        response = client.delete("/leads/1")
        assert response.status_code == 404

def test_lead_deletado_nao_aparece_na_listagem(client):
    with patch("controllers.lead.get_all_leads", return_value=[]), \
         patch("controllers.lead.count_all_leads", return_value=0):
        response = client.get("/leads/")
        assert response.status_code == 200
        assert response.json()["data"] == []
        assert response.json()["total"] == 0

