from jose import jwt, JWTError
import datetime
import environs

from src.settings import settings


def generate_token(payload: dict, token_type: str = None) -> dict:
    """
    Generate JWT tokens based on the provided payload. If token_type is None, both access and refresh tokens are generated.

    Parameters:
    payload (dict): A dictionary containing the token's payload. It should include the user's information.
    token_type (str or None): The type of token to generate. It can be 'access', 'refresh', or None (for both).

    Returns:
    dict: A dictionary containing the generated JWT tokens.

    Raises:
    ValueError: If the token_type is invalid and not None.
    """
    exp_times = {
        "access": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=settings.ACCESS_EXP_MINUTES),
        "refresh": datetime.datetime.utcnow()
        + datetime.timedelta(days=settings.REFRESH_EXP_DAYS),
    }

    # If token_type is provided, generate the requested token
    if token_type:
        if token_type not in exp_times:
            raise ValueError(f"Invalid token type: {token_type}")
        payload["exp"] = exp_times[token_type]
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return {f"{token_type}_token": token}

    # If no token_type is provided, generate both access and refresh tokens
    tokens = {}
    for t_type, exp_time in exp_times.items():  
        payload["exp"] = exp_time
        tokens[f"{t_type}_token"] = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    return tokens


def decode_token(token: str, token_type: str = None) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Token verification failed ({token_type}): {str(e)}")


def refresh_access_token(refresh_token: str) -> str:
    payload = decode_token(refresh_token, token_type="refresh")
    # Remove the exp field from the payload before generating a new access token
    if "exp" in payload:
        del payload["exp"]
    return generate_access_token(payload)
