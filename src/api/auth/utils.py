from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import load_only
import bcrypt

from src.db.models.auth import User
from .jwt import decode_token
from src.db.config import get_db
from src.logger import logger


def hash_password(password: str) -> str:
    # Encode the password to bytes before hashing
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password, hashed_password)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        logger.info(payload)

        # Assuming you're filtering users by UUID
        user = (
            db.query(User)
            .options(
                load_only(
                    User.uuid,
                    User.username,
                    User.email,
                    User.telegram_id,
                    User.telegram_username,
                    User.is_superuser,
                )
            )
            .filter(User.uuid == payload["user_id"])
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        logger.info(f"Authenticated user: {user}")
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )


def authenticate(username, password):
    user = (
        db.query(User)
        .options(load_only(User.uuid, User.password))
        .filter(User.username == username)
        .first()
    )

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user
