from fastapi import Depends
from fastapi.routing import APIRouter

from src.api.auth.schemes import UserScheme


router = APIRouter(prefix="/notes")


@router.post("/create")
async def create_note_handler(
    note: NoteScheme, user: UserScheme = Depends(get_current_user)
):
    pass
