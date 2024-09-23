from jose import jwt, JWTError
import datetime
import environs

from src.settings import settings


def generate_token(payload: dict, token_type: str) -> str:
    """
    Generate a JWT token based on the provided payload and token type.

    Parameters:
    payload (dict): A dictionary containing the token's payload. It should include the user's information.
    token_type (str): The type of token to generate. It can be either 'access' or 'refresh'.

    Returns:
    str: The generated JWT token.

    Raises:
    ValueError: If the token_type is not 'access' or 'refresh'.
    """
    exp = {
        "access": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=settings.ACCESS_EXP_MINUTES),
        "refresh": datetime.datetime.utcnow()
        + datetime.timedelta(days=settings.REFRESH_EXP_DAYS),
    }

    if token_type not in exp:
        raise ValueError(f"Invalid token type: {token_type}")
    payload["exp"] = exp[token_type]
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_token(token: str, secret_key: str, token_type: str = "access") -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError as e:
        raise JWTError(f"Token verification failed ({token_type}): {str(e)}")


def refresh_access_token(refresh_token: str) -> str:
    payload = verify_token(refresh_token, REFRESH_TOKEN_SECRET, token_type="refresh")
    # Remove the exp field from the payload before generating a new access token
    if "exp" in payload:
        del payload["exp"]
    return generate_access_token(payload)
