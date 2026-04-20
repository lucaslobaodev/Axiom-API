from fastapi import APIRouter, HTTPException, Request, Depends, Query
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas.lead import Lead
from schemas.lead_response import LeadResponse
from schemas.lead_list_response import PaginatedLeadResponse
from schemas.lead_query import LeadOrderBy, SortDirection
from services.lead import create_lead
from repository.lead import get_all_leads, get_leads_by_email, get_leads_by_phone, get_lead_by_id, soft_delete_lead, count_all_leads
from core.auth import require_api_key


limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/leads", tags=["leads"], dependencies=[Depends(require_api_key)])

@router.post("/", response_model=LeadResponse)
@limiter.limit("10/minute")
def post_lead(request: Request, lead: Lead):
    return create_lead(lead)

@router.get("/", response_model=PaginatedLeadResponse)
@limiter.limit("30/minute")
def list_leads(
    request: Request,
    email: str = None,
    phone: str = None,
    phone_contains: str = None,
    order_by: LeadOrderBy = LeadOrderBy.id,
    direction: SortDirection = SortDirection.asc,
    limit: int = Query(default=20, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
):
    if email:
        result = get_leads_by_email(email)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum lead encontrado com esse email")
        return PaginatedLeadResponse(data=result, total=len(result), limit=limit, offset=offset)
    if phone:
        result = get_leads_by_phone(phone)
        if not result:
            raise HTTPException(status_code=404, detail="Nenhum lead encontrado com esse telefone")
        return PaginatedLeadResponse(data=result, total=len(result), limit=limit, offset=offset)
    data = get_all_leads(limit=limit, offset=offset, order_by=order_by.value, direction=direction.value, phone_contains=phone_contains)
    total = count_all_leads(phone_contains=phone_contains)
    return PaginatedLeadResponse(data=data, total=total, limit=limit, offset=offset)

@router.get("/{lead_id}", response_model=LeadResponse)
@limiter.limit("30/minute")
def get_lead(request: Request, lead_id: int):
    result = get_lead_by_id(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return result[0]

@router.delete("/{lead_id}", status_code=204)
@limiter.limit("30/minute")
def delete_lead(request: Request, lead_id: int):
    result = soft_delete_lead(lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
