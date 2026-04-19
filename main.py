from fastapi import FastAPI
from controllers.lead import router as lead_router

app = FastAPI()

app.include_router(lead_router)
