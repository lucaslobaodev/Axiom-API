from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key")

def require_api_key(key: str = Security(api_key_header)):
    if key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="API key inválida")
