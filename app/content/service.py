from sqlalchemy import select
from sqlalchemy.orm import Session

from app.content.exceptions import MsczContentNotFoundException
from app.content.models import MsczContent


def _file_url(file_id: int) -> str:
    return f"/api/static_content/{file_id}"


def create_mscz_content(
    session: Session,
    c_mscz_file_id: int,
    c_svg_file_id: int,
    pdf_file_id: int,
    mp3_file_id: int | None = None,
) -> dict:
    mscz = MsczContent(
        c_mscz_file_id=c_mscz_file_id,
        c_svg_file_id=c_svg_file_id,
        pdf_file_id=pdf_file_id,
        mp3_file_id=mp3_file_id,
    )
    session.add(mscz)
    session.commit()
    return _mscz_to_dict(mscz)


def get_mscz_content(session: Session, mscz_id: int) -> dict:
    mscz = session.scalars(
        select(MsczContent).where(MsczContent.id == mscz_id)
    ).first()
    if mscz is None:
        raise MsczContentNotFoundException("MuseScore content not found")
    return _mscz_to_dict(mscz)


def _mscz_to_dict(mscz: MsczContent) -> dict:
    return {
        "id": mscz.id,
        "c_mscz_file_id": mscz.c_mscz_file_id,
        "c_svg_file_id": mscz.c_svg_file_id,
        "pdf_file_id": mscz.pdf_file_id,
        "mp3_file_id": mscz.mp3_file_id,
        "svg_url": _file_url(mscz.c_svg_file_id),
        "pdf_url": _file_url(mscz.pdf_file_id),
        "mscz_url": _file_url(mscz.c_mscz_file_id),
        "mp3_url": _file_url(mscz.mp3_file_id) if mscz.mp3_file_id else None,
        "added_at": mscz.added_at.isoformat() if mscz.added_at else None,
    }
