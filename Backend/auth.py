from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserRegister, UserLogin
from typing import Dict
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

users_db: Dict[str, str] = {}     # username -> password (plaintext, demo only)
tokens_db: Dict[str, str] = {}    # token -> username

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return tokens_db[token]

async def register_user(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user.password
    logger.info(f"Registered new user: {user.username}")
    return {"message": "User registered successfully"}

async def login_user(user: UserLogin):
    if users_db.get(user.username) != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = str(uuid4())
    tokens_db[token] = user.username
    logger.info(f"User logged in: {user.username} Token: {token}")
    return {"token": token}
