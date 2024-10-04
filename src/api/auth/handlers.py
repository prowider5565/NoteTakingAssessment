from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.routing import APIRouter
from fastapi import Depends, status

from .utils import hash_password, get_current_user, authenticate
from .schemes import UserScheme, LoginScheme
from src.db.models.auth import User
from src.db.config import get_db
from .jwt import generate_token
from src.logger import logger


auth_router = APIRouter(prefix="/accounts")

from .jwt import generate_token  # Assuming you have a token generation function


@auth_router.post("/register")
async def register_user(user: UserScheme, db=Depends(get_db)):
    """
    Registers a new user in the system and returns a token with the user's uuid in the payload.
    """
    try:
        user_details = user.dict()
        user_details["password"] = hash_password(user_details["password"])
        logger.info("User: " + str(user_details))

        new_user = User(**user_details)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Add the user's uuid to the payload
        payload = {"user_id": str(new_user.uuid)}
        token = generate_token(payload)

    except IntegrityError:
        raise HTTPException(
            detail="Email or username already exists!",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return JSONResponse(
        {"message": "User registered successfully", "token": token},
        status_code=status.HTTP_201_CREATED,
    )


@auth_router.post("/login")
async def login_user(login: LoginScheme, db=Depends(get_db)):
    login_details = login.dict()
    authenticated = authenticate(db=db, **login_details)
    if authenticated:
        payload = {"user_id": str(authenticated.uuid)}
        token = generate_token(payload)
        return JSONResponse({"message": "Logged in successfully!", "token": token})


@auth_router.get("/details")
async def get_user_details(current_user=Depends(get_current_user)):
    return current_user
