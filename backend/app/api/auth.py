from hashlib import pbkdf2_hmac
from hmac import compare_digest
from secrets import token_hex
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/auth", tags=["Authentication"])

_users: dict[str, dict[str, str]] = {}
_tokens: dict[str, str] = {}


def _password_hash(password: str, salt: str) -> str:
    digest = pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return digest.hex()


def _public_user(user: dict[str, str]) -> dict[str, str]:
    return {"email": user["email"], "name": user["name"]}


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterRequest(Credentials):
    name: str = Field(min_length=2, max_length=80)


class AuthResponse(BaseModel):
    token: str
    user: dict[str, str]


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> dict[str, str]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    token = authorization.split(" ", 1)[1].strip()
    email = _tokens.get(token)
    user = _users.get(email or "")
    if not user:
        raise HTTPException(status_code=401, detail="Your session has expired. Sign in again.")
    return user


@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest):
    email = request.email.lower()
    if email in _users:
        raise HTTPException(status_code=409, detail="An account with that email already exists.")
    salt = token_hex(16)
    user = {"email": email, "name": request.name.strip(), "salt": salt, "password": _password_hash(request.password, salt)}
    _users[email] = user
    token = token_hex(32)
    _tokens[token] = email
    return {"token": token, "user": _public_user(user)}


@router.post("/login", response_model=AuthResponse)
def login(request: Credentials):
    email = request.email.lower()
    user = _users.get(email)
    if not user or not compare_digest(user["password"], _password_hash(request.password, user["salt"])):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    token = token_hex(32)
    _tokens[token] = email
    return {"token": token, "user": _public_user(user)}


@router.get("/me")
def me(user: Annotated[dict[str, str], Depends(get_current_user)]):
    return {"user": _public_user(user)}


@router.post("/logout")
def logout(authorization: Annotated[str | None, Header()] = None):
    if authorization and authorization.lower().startswith("bearer "):
        _tokens.pop(authorization.split(" ", 1)[1].strip(), None)
    return {"success": True}
