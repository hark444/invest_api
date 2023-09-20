from fastapi import APIRouter
from .routes import user, user_roles, auth, equity_dividends, fixed_deposits

version_router = APIRouter(prefix="/v1")
version_router.include_router(user.user_router)
version_router.include_router(auth.auth_router)
version_router.include_router(user_roles.user_role_router)
version_router.include_router(equity_dividends.equity_dividends_router)
version_router.include_router(fixed_deposits.fixed_deposit_router)
