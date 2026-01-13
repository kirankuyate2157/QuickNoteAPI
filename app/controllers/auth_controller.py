import time
from app.schemas.auth_schema import LoginRequest
from app.store.memory import token_store


def mock_login(payload: LoginRequest):
    token = f"token_{payload.userId}_{int(time.time())}"
    token_store[token] = payload.userId
    return {"token": token}
