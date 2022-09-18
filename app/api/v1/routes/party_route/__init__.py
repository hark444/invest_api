from fastapi import Depends, APIRouter, HTTPException, status
from app.api.v1.routes.auth import oauth2_scheme
from app.api.v1.routes.party_route.party import party_party_router
from app.api.v1.routes.party_route.parties_attended import parties_attended_router

PROTECTED = [Depends(oauth2_scheme)]

party_router = APIRouter(prefix="/user/{user_id}", dependencies=PROTECTED)
party_router.include_router(party_party_router)
party_router.include_router(parties_attended_router)
