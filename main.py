from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from controllers.lead import router as lead_router
from controllers.health import router as health_router
from core.middleware import logging_middleware

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.middleware("http")(logging_middleware)

app.include_router(lead_router)
app.include_router(health_router)
