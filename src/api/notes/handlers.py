from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from .schemes import NoteScheme, NoteUpdateScheme, NoteResponseScheme
from src.api.auth.utils import get_current_user
from src.db.models.notes import Notes
from src.db.models.auth import User
from src.db.config import get_db

router = APIRouter(prefix="/notes")


@router.post("/create", response_model=NoteResponseScheme)
async def create_note_handler(
    note: NoteScheme,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Creates a new note for the authenticated user.
    """
    new_note = Notes(title=note.title, content=note.content, author_id=user.uuid)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/", response_model=list[NoteResponseScheme])
async def list_notes_handler(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    """
    Lists all notes belonging to the authenticated user.
    """
    notes = db.query(Notes).filter(Notes.author_id == user.uuid).all()
    return notes


@router.get("/{note_id}", response_model=NoteResponseScheme)
async def get_note_handler(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Retrieves a single note by ID, only if it belongs to the authenticated user.
    """
    note = (
        db.query(Notes)
        .filter(Notes.uuid == note_id, Notes.author_id == user.uuid)
        .first()
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.put("/{note_id}", response_model=NoteResponseScheme)
async def update_note_handler(
    note_id: uuid.UUID,
    note: NoteScheme,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Updates a note if it belongs to the authenticated user.
    """
    existing_note = (
        db.query(Notes)
        .filter(Notes.uuid == note_id, Notes.author_id == user.uuid)
        .first()
    )
    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    existing_note.title = note.title
    existing_note.content = note.content
    db.commit()
    db.refresh(existing_note)
    return existing_note


@router.patch("/{note_id}", response_model=NoteResponseScheme)
async def partial_update_note_handler(
    note_id: uuid.UUID,
    note: NoteUpdateScheme,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Partially updates a note if it belongs to the authenticated user.
    """
    existing_note = (
        db.query(Notes)
        .filter(Notes.uuid == note_id, Notes.author_id == user.uuid)
        .first()
    )
    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    if note.title is not None:
        existing_note.title = note.title
    if note.content is not None:
        existing_note.content = note.content
    db.commit()
    db.refresh(existing_note)
    return existing_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_handler(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Deletes a note if it belongs to the authenticated user.
    """
    existing_note = (
        db.query(Notes)
        .filter(Notes.uuid == note_id, Notes.author_id == user.uuid)
        .first()
    )
    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    db.delete(existing_note)
    db.commit()
    return None
