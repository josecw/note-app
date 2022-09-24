
import time
from typing import Dict
from jose import JWTError, jwt

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder

from core.config import settings
from core.models.auth import TokenData
from core.models.user import User

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGO


def token_response(token: str):
    return {
        "token": token
    }

def signJWT(tokenData: TokenData) -> Dict[str, str]:

    jwt_token = jwt.encode(jsonable_encoder(tokenData), JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(jwt_token)


def decodeJWT(token: str) -> Dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        return decoded_token if decoded_token["expired_dt"] >= time.time() is not None else None
    except:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid Token")
            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid Token")

    async def verify_jwt(self, token: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(token)
            username = payload.get('username')
            tokenData = await TokenData.select(ids=[username])
        except:
            tokenData = None
        if tokenData:
            isTokenValid = True
        return isTokenValid


async def get_current_user(token: str = Depends(JWTBearer())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = decodeJWT(token)
        username: str = payload.get("username")
        
    except JWTError:
        raise credentials_exception
    user = await User.find_one(User.username == username)
    if user is None:
        raise credentials_exception
    return user
