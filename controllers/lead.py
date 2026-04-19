from fastapi import APIRouter, HTTPException
from schemas.lead import Lead
from services.lead import create_lead
from repository.lead import get_all_leads, get_leads_by_email, get_leads_by_phone, get_lead_by_id

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/")
def post_lead(lead: Lead):
    create_lead(lead)
    return {"message": "Lead criado com sucesso"}

@router.get("/")
def list_leads(email: str = None, phone: str = None):
    if email:
        result = get_leads_by_email(email)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum lead encontrado com esse email")
        return result
    if phone:
        result = get_leads_by_phone(phone)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum lead encontrado com esse telefone")
        return result
    return get_all_leads()

@router.get("/{lead_id}")
def get_lead(lead_id: int):
    result = get_lead_by_id(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return result[0]
