from typing import Annotated

from fastapi import APIRouter, Depends

from app.content import service
from app.content.schema import MsczContentCreate, MsczContentRead
from app.database import DbSessionDep
from app.user.schema import UserInDb
from app.user.service import get_current_user

content_router = APIRouter(
    prefix="/content",
    tags=["Content"],
    responses={404: {"description": "Not found"}},
)


@content_router.post("/mscz", response_model=MsczContentRead)
def create_mscz(
    session: DbSessionDep,
    body: MsczContentCreate,
    _current_user: Annotated[UserInDb, Depends(get_current_user)],
):
    return service.create_mscz_content(
        session,
        c_mscz_file_id=body.c_mscz_file_id,
        c_svg_file_id=body.c_svg_file_id,
        pdf_file_id=body.pdf_file_id,
        mp3_file_id=body.mp3_file_id,
    )


@content_router.get("/mscz/{mscz_id}", response_model=MsczContentRead)
def get_mscz(session: DbSessionDep, mscz_id: int):
    return service.get_mscz_content(session, mscz_id)
