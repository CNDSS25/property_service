import jwt
from fastapi import FastAPI, HTTPException, Depends, status, Body
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

# class JWTAdapter:
#     """
#     Adapter für das JWT-Handling.
#     """
#
#     def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
#         """
#         Konstruktor für den JWT-Adapter.
#
#         :param secret_key: Der geheime Schlüssel für die JWT-Generierung
#         :param algorithm: Der Algorithmus für die JWT-Generierung
#         :param expire_minutes: Die Gültigkeitsdauer des Tokens in Minuten
#         """
#         self.secret_key = secret_key
#         self.algorithm = algorithm
#         self.expire_minutes = expire_minutes


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
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing 'sub'"
        )
    # user = fake_users_db.get(username)
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User not found"
    #     )

