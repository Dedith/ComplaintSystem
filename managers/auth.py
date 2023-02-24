import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import user
from db import database
from starlette.requests import Request
from typing import Optional
from fastapi import HTTPException
from models import RoleType


class AuthManager:
   # @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": (datetime.utcnow() + timedelta(minutes=60))
            }
            print(config)
            return jwt.encode(payload, config("SECRET_WORD"), algorithm="HS256")
        except Exception as ex:
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        print(config)

        try:
            payload = jwt.decode(res.credentials, config(
                "SECRET_WORD"), algorithms=["HS256"])
            user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid Token")


oauth2_scheme = CustomHTTPBearer()


def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")
