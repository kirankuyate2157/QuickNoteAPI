from pydantic import BaseModel, Field
from typing import Optional


class NoteCreateSchema(BaseModel):
    title: str = Field(
        ...,
        # min_length=1,
        max_length=80,
        description="Note title"
    )
    body: Optional[str] = Field(
        None,
        max_length=500,
        description="Some Notes "
    )


class NoteUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        None,
        max_length=80
    )
    body: Optional[str] = Field(
        None,
        max_length=500
    )
