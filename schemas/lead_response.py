from pydantic import BaseModel

class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
