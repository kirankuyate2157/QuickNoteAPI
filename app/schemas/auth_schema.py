from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    userId: str = Field(
        ...,
        min_length=1,
        description="Unique user identifier"
    )