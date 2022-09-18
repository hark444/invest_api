from fastapi import FastAPI
from app.api import api_router


application = FastAPI()
application.include_router(api_router)
