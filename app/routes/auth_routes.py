
from fastapi import APIRouter
from app.controllers.auth_controller import mock_login
from app.schemas.auth_schema import LoginRequest

router = APIRouter(prefix="/auth")

@router.post("/mock-login")
def login(payload: LoginRequest):
    return mock_login(payload)
