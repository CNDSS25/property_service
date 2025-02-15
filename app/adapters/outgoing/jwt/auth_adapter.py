import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

def decode_token(token: str) -> dict:
    """
    Dekodiert ein JWT-Zugriffstoken.

    :param token: Das JWT-Token
    :return: Die im Token enthaltenen Daten
    :raises: JWTError, wenn das Token ungültig oder abgelaufen ist
    """
    return jwt.decode(token,'secret_key_example', algorithms=['HS256'])

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Decode the token and retrieve the current user.
    Also verifies that the token includes the required claims.
    """
    token = credentials.credentials

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )