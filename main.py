import uvicorn
from fastapi import FastAPI
from app.api import api_router
from settings import settings


application = FastAPI()
application.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(application, host=settings.API.LOCALHOST, port=settings.API.LOCAL_PORT)
