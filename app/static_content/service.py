import bz2
import os
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import StaticContentFileTypes, app_settings
from app.static_content.exceptions import (
    InvalidFileTypeException,
    StaticContentNotFoundException,
)
from app.static_content.models import StaticContent

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {ft.value for ft in StaticContentFileTypes}


def _get_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower()


def store_file(session: Session, filename: str, content: bytes) -> dict:
    ext = _get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise InvalidFileTypeException(
            f"File type '{ext}' not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    unique_name = f"{uuid.uuid4().hex}.{ext}.bz"
    rel_path = f"{app_settings.static_content_prefix}/{unique_name}"

    os.makedirs(app_settings.static_content_prefix, exist_ok=True)
    compressed = bz2.compress(content)
    with open(rel_path, "wb") as f:
        f.write(compressed)

    sc = StaticContent(path=rel_path)
    session.add(sc)
    session.commit()

    return {
        "id": sc.id,
        "path": sc.path,
        "filename": filename,
    }


def get_file(session: Session, file_id: int) -> tuple[bytes, str]:
    sc = session.scalars(
        select(StaticContent).where(StaticContent.id == file_id)
    ).first()
    if sc is None:
        raise StaticContentNotFoundException("File not found")

    if not os.path.exists(sc.path):
        raise StaticContentNotFoundException("File not found on disk")

    with open(sc.path, "rb") as f:
        compressed = f.read()

    data = bz2.decompress(compressed)

    # Extract extension from path pattern: /prefix/uuid.ext.bz
    basename = os.path.basename(sc.path)
    ext = basename.rsplit(".", 2)[-2] if basename.count(".") >= 2 else ""

    return data, ext


def get_file_info(session: Session, file_id: int) -> dict:
    sc = session.scalars(
        select(StaticContent).where(StaticContent.id == file_id)
    ).first()
    if sc is None:
        raise StaticContentNotFoundException("File not found")

    return {"id": sc.id, "path": sc.path}


def delete_file(session: Session, file_id: int) -> None:
    sc = session.scalars(
        select(StaticContent).where(StaticContent.id == file_id)
    ).first()
    if sc is None:
        raise StaticContentNotFoundException("File not found")

    if os.path.exists(sc.path):
        os.remove(sc.path)

    session.delete(sc)
    session.commit()
