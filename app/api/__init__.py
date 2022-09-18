from fastapi import APIRouter
from app.api.v1 import version_router as v1_router

# from app.auth.inter_service_auth import verify_auth_token


# PROTECTED = [Depends(verify_auth_token)]


# api_router = APIRouter(prefix="/api", dependencies=PROTECTED)
api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
