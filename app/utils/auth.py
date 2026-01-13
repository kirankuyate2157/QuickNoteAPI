from fastapi import Header, HTTPException
from app.store.memory import token_store


def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={"error": "Authorization header missing"}
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid authorization format"}
        )

    token = authorization.replace("Bearer ", "").strip()
    user_id = token_store.get(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid or expired token"}
        )

    return user_id
