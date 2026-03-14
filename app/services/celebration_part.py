from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.celebration_part import (
    db_create_celebration_part,
    db_delete_celebration_part,
    db_get_celebration_part_by_id,
    db_get_celebration_parts,
    db_update_celebration_part,
)
from app.models.celebration_part import CelebrationPart
from app.schemas.celebration_part import (
    CelebrationPart as CelebrationPartSchema,
    CelebrationPartCreate,
    CelebrationPartUpdate,
)


def get_celebration_parts(
    db: Session, pagination: PaginationParams,
) -> Paginated[CelebrationPartSchema]:
    total, items = db_get_celebration_parts(
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


def get_celebration_part_by_id(part_id: int, db: Session) -> CelebrationPartSchema:
    part = db_get_celebration_part_by_id(part_id, db)
    if not part:
        raise NotFoundError("CelebrationPart")
    return part


def create_celebration_part(
    data: CelebrationPartCreate, db: Session,
) -> CelebrationPartSchema:
    part = CelebrationPart(name=data.name, order_index=data.order_index)
    return db_create_celebration_part(part, db)


def update_celebration_part(
    part_id: int, data: CelebrationPartUpdate, db: Session,
) -> CelebrationPartSchema:
    part = db_get_celebration_part_by_id(part_id, db)
    if not part:
        raise NotFoundError("CelebrationPart")
    part.name = data.name
    part.order_index = data.order_index
    return db_update_celebration_part(part, db)


def delete_celebration_part(part_id: int, db: Session) -> CelebrationPartSchema:
    part = db_get_celebration_part_by_id(part_id, db)
    if not part:
        raise NotFoundError("CelebrationPart")
    return db_delete_celebration_part(part, db)

