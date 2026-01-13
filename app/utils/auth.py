from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.store.memory import token_store

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401, detail={"error": "Authorization header missing"}
        )

    if not token.startswith("token"):
        raise HTTPException(
            status_code=401, detail={"error": "Invalid authorization format"}
        )

    user_id = token_store.get(token)

    if not user_id:
        raise HTTPException(
            status_code=401, detail={"error": "Invalid or expired token"}
        )

    return user_id
