from fastapi import APIRouter, Depends, status

from app.utils.auth import get_current_user
from app.schemas.note_schema import NoteCreateSchema, NoteUpdateSchema
from app.controllers.notes_controller import (
    create_note,
    list_notes,
    update_note,
    delete_note
)

router = APIRouter(prefix="/notes")


@router.post("", status_code=status.HTTP_201_CREATED)
def create(payload: NoteCreateSchema, user_id: str = Depends(get_current_user)):
    return create_note(payload, user_id)


@router.get("")
def get_all(user_id: str = Depends(get_current_user)):
    return list_notes(user_id)


@router.patch("/{note_id}")
def update(note_id: str, payload: NoteUpdateSchema, user_id: str = Depends(get_current_user)):
    return update_note(note_id, payload, user_id)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(note_id: str, user_id: str = Depends(get_current_user)):
    delete_note(note_id, user_id)
    return None
