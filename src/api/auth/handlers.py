from fastapi.routing import APIRouter


auth_router = APIRouter(prefix="accounts")


@auth_router.post("/register")
async def register_user(user: UserScheme):
    """
    Registers a new user in the system.
    """
    