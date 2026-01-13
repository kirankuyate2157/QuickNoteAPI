from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException

from app.store.memory import notes_by_id, notes_by_user, storage_lock
from app.schemas.note_schema import NoteCreateSchema, NoteUpdateSchema


def create_note(payload: NoteCreateSchema, user_id: str):
    note_id = str(uuid4())
    now = datetime.utcnow().isoformat()

    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail={"error": "Title is required"})

    note = {
        "id": note_id,
        "title": title,
        "body": payload.body,
        "userId": user_id,
        "createdAt": now,
        "updatedAt": None,
    }

    with storage_lock:
        notes_by_id[note_id] = note
        notes_by_user.setdefault(user_id, set()).add(note_id)

    return note


def list_notes(user_id: str):
    note_ids = notes_by_user.get(user_id, set())
    notes = [notes_by_id[nid] for nid in note_ids]
    # 
    # newest first
    return sorted(notes, key=lambda x: x["createdAt"], reverse=True)


def update_note(note_id: str, payload: NoteUpdateSchema, user_id: str):
    note = notes_by_id.get(note_id)

    if not note:
        raise HTTPException(status_code=404, detail={"error": "Note not found"})

    if note["userId"] != user_id:
        raise HTTPException(status_code=403, detail={"error": "Forbidden"})

    if payload.title is None and payload.body is None:
        raise HTTPException(status_code=400, detail={"error": "No fields to update"})

    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail={"error": "Title is required"})
        note["title"] = title

    if payload.body is not None:
        note["body"] = payload.body

    note["updatedAt"] = datetime.utcnow().isoformat()
    return note


def delete_note(note_id: str, user_id: str):
    note = notes_by_id.get(note_id)

    if not note:
        raise HTTPException(status_code=404, detail={"error": "Note not found"})

    if note["userId"] != user_id:
        raise HTTPException(status_code=403, detail={"error": "Forbidden"})

    with storage_lock:
        del notes_by_id[note_id]
        notes_by_user[user_id].remove(note_id)
