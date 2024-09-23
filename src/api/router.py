from fastapi.routing import APIRouter

from .auth.handlers import auth_router


router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
