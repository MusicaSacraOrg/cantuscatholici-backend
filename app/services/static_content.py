import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import NotFoundError
from app.common.schemas.pagination import Paginated
from app.config import storage_settings
from app.db.static_content import (
    db_create_static_content,
    db_delete_static_content,
    db_get_static_content_by_id,
    db_get_static_contents,
)
from app.models.content_base import ContentBase
from app.models.static_content import StaticContent
from app.schemas.static_content import StaticContentRead


def get_static_contents(db: Session, pagination: PaginationParams) -> Paginated[StaticContentRead]:
    total, items = db_get_static_contents(
        db,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
    )
    return Paginated(
        total=total,
        limit=pagination.limit or 100,
        offset=pagination.offset,
        order=pagination.order,
        order_by=pagination.order_by,
        items=items,
    )


def get_static_content_by_id(static_content_id: int, db: Session) -> StaticContentRead:
    item = db_get_static_content_by_id(static_content_id, db)
    if not item:
        raise NotFoundError("StaticContent")
    return item


async def upload_static_content(file: UploadFile, db: Session) -> StaticContentRead:
    upload_dir = Path(storage_settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename).suffix if file.filename else ""
    filename = f"{uuid.uuid4().hex}{suffix}"
    file_path = upload_dir / filename

    contents = await file.read()
    file_path.write_bytes(contents)

    relative_path = str(file_path.relative_to(upload_dir.parent))

    content_base = ContentBase()
    db.add(content_base)
    db.flush()

    static_content = StaticContent(
        content_base_id=content_base.id,
        path=relative_path,
    )
    return db_create_static_content(static_content, db)


def delete_static_content(static_content_id: int, db: Session) -> StaticContentRead:
    item = db_get_static_content_by_id(static_content_id, db)
    if not item:
        raise NotFoundError("StaticContent")

    file_path = Path(storage_settings.upload_dir).parent / item.path
    if file_path.exists():
        file_path.unlink(missing_ok=True)

    return db_delete_static_content(item, db)

