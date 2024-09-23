from fastapi.routing import APIRouter

from .schemes import UserScheme
from src.logger import logger


auth_router = APIRouter(prefix="/accounts")


@auth_router.post("/register")
async def register_user(user: UserScheme):
    """
    Registers a new user in the system.
    """
    user_details = user.dict()
    logger.info("User: " + str(user_details))
