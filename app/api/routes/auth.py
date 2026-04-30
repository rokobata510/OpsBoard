import base64
import binascii
import hashlib
import hmac
import json
import os
import time

from fastapi import APIRouter, Depends, Header, HTTPException
from app.schemas.user import UserUnhashed
import bcrypt

from app.db.database import get_connection

router = APIRouter()
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
ACCESS_TOKEN_EXPIRES_SECONDS = 60 * 60


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("utf-8")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def create_access_token(user_id: int, email: str) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT",
    }
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRES_SECONDS,
    }

    encoded_header = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _base64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(
        JWT_SECRET.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    return f"{signing_input}.{_base64url_encode(signature)}"


def decode_access_token(token: str) -> dict:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

    signing_input = f"{encoded_header}.{encoded_payload}"
    expected_signature = hmac.new(
        JWT_SECRET.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    try:
        actual_signature = _base64url_decode(encoded_signature)
    except (binascii.Error, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    if not hmac.compare_digest(actual_signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        payload = json.loads(_base64url_decode(encoded_payload))
    except (binascii.Error, json.JSONDecodeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("exp") is None or payload["exp"] < int(time.time()):
        raise HTTPException(status_code=401, detail="Token expired")
    if payload.get("sub") is None or payload.get("email") is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    payload = decode_access_token(authorization.removeprefix("Bearer ").strip())
    return {
        "id": int(payload["sub"]),
        "email": payload["email"],
    }

@router.post("/register")
def register(payload: UserUnhashed):
    
    if payload.email is None:
        raise HTTPException(status_code=422, detail="No email provided")
    if payload.password_plaintext is None: 
        raise HTTPException(status_code=422, detail="No password provided")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select email from users where email ilike %s
                """
                , (payload.email,)
            )
            if (cur.fetchone() is not None):
                raise HTTPException(status_code=409, detail="User already exists")
            password_hashed = bcrypt.hashpw(
                payload.password_plaintext.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
            cur.execute(
                """
                insert into users (email, password_hash)
                values (%s, %s)
                returning id, email
                """
                , (payload.email, password_hashed,)
            )
            row = cur.fetchone()
            return {
                "status": "success", 
                "user": {
                    "id": row[0],
                    "email": row[1],
                }
            }
@router.post("/login")
def login(payload: UserUnhashed):
    if payload.email is None:
        raise HTTPException(status_code=422, detail="No email provided")
    if payload.password_plaintext is None: 
        raise HTTPException(status_code=422, detail="No password provided")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, email, password_hash from users where email ilike %s
                """
                , (payload.email,)
            )
            row = cur.fetchone()
            if (row is None):
                raise HTTPException(status_code=409, detail="User does not exist")
            if( bcrypt.checkpw(
                payload.password_plaintext.encode("utf-8"),
                row[2].encode("utf-8")
            )):
                access_token = create_access_token(row[0], row[1])
                return {
                    "status": "success", 
                    "user": {
                        "id": row[0],
                        "email": row[1],
                    },
                    "access_token": access_token,
                    "token_type": "bearer",
                }
            raise HTTPException(status_code=401, detail="Incorrect Password")


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return {
        "status": "success",
        "user": current_user,
    }
