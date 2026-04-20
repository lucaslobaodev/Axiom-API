from typing import List
from pydantic import BaseModel
from schemas.lead_response import LeadResponse

class PaginatedLeadResponse(BaseModel):
    data: List[LeadResponse]
    total: int
    limit: int
    offset: int
