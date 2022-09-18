from fastapi import APIRouter
from .routes import user, user_roles, auth
from .routes.party_route import party_router

version_router = APIRouter(prefix="/v1")
version_router.include_router(user.user_router)
version_router.include_router(auth.auth_router)
version_router.include_router(user_roles.user_role_router)
version_router.include_router(party_router)
