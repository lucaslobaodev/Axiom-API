from fastapi import APIRouter, HTTPException, Request, Depends
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas.lead import Lead
from schemas.lead_response import LeadResponse
from services.lead import create_lead
from repository.lead import get_all_leads, get_leads_by_email, get_leads_by_phone, get_lead_by_id
from core.auth import require_api_key

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/leads", tags=["leads"], dependencies=[Depends(require_api_key)])

@router.post("/", response_model=LeadResponse)
@limiter.limit("10/minute")
def post_lead(request: Request, lead: Lead):
    try:
        return create_lead(lead)
    except ValueError as e:
        if str(e) == "duplicate":
            raise HTTPException(status_code=409, detail="Email ou telefone já cadastrado")
        raise

@router.get("/", response_model=List[LeadResponse])
@limiter.limit("30/minute")
def list_leads(request: Request, email: str = None, phone: str = None, limit: int = 20, offset: int = 0):
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
    return get_all_leads(limit=limit, offset=offset)

@router.get("/{lead_id}", response_model=LeadResponse)
@limiter.limit("30/minute")
def get_lead(request: Request, lead_id: int):
    result = get_lead_by_id(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return result[0]
