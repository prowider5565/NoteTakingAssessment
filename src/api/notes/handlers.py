from fastapi import Depends
from fastapi.routing import APIRouter

from .schemes import NoteScheme


router = APIRouter(prefix="/notes")


@router.post("/create")
async def create_note_handler(note: NoteScheme, user=Depends(get_current_user)):
    """
    Creates a new note for the authenticated user.
    """
    