import pytest
from schemas.lead import Lead

BASE = {"name": "Lucas", "email": "lucas@test.com"}

def test_lead_valid():
    lead = Lead(**BASE, phone="11999998888")
    assert lead.phone == "11999998888"

def test_phone_short():
    with pytest.raises(Exception):
        Lead(**BASE, phone="123")

def test_phone_sem_ddd_valido():
    with pytest.raises(Exception):
        Lead(**BASE, phone="00999998888")

def test_phone_formato_mascara():
    lead = Lead(**BASE, phone="(11)99999-8888")
    assert lead.phone == "11999998888"

def test_phone_plus_sem_pais():
    with pytest.raises(Exception):
        Lead(**BASE, phone="+11999998888")

def test_phone_com_plus_55():
    lead = Lead(**BASE, phone="+5511999998888")
    assert lead.phone == "11999998888"
