from fastapi.routing import APIRouter

from .notes.handlers import router as note_router
from .auth.handlers import auth_router


router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(note_router)
