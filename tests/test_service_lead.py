from unittest.mock import patch, MagicMock
from schemas.lead import Lead
from services.lead import create_lead

BASE_LEAD_DB = {"id": 1, "name": "Lucas", "email": "lucas@test.com", "phone": "+5511999998888"}

def _make_lead():
    return Lead(name="Lucas", email="lucas@test.com", phone="11999998888")

def test_create_lead_novo():
    with patch("services.lead.insert_lead", return_value=[BASE_LEAD_DB]):
        result = create_lead(_make_lead())
        assert result["email"] == BASE_LEAD_DB["email"]

def test_create_lead_duplicado_retorna_existente():
    with patch("services.lead.insert_lead", side_effect=ValueError("duplicate")), \
         patch("services.lead.get_leads_by_email", return_value=[BASE_LEAD_DB]) as mock_get:
        result = create_lead(_make_lead())
        assert result["id"] == 1
        mock_get.assert_called_once_with("lucas@test.com")

def test_create_lead_erro_desconhecido_propaga():
    with patch("services.lead.insert_lead", side_effect=ValueError("outro erro")):
        try:
            create_lead(_make_lead())
            assert False, "deveria ter levantado ValueError"
        except ValueError as e:
            assert str(e) == "outro erro"
