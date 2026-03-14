from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.deps.pagination import PaginationParams
from app.common.exceptions import AlreadyExistsError, NotFoundError
from app.common.schemas.pagination import Paginated
from app.db.celebration_category import (
    db_create_celebration_category,
    db_delete_celebration_category,
    db_get_celebration_categories,
    db_get_celebration_category_by_id,
    db_update_celebration_category,
)
from app.models.celebration_category import CelebrationCategory
from app.schemas.celebration_category import (
    CelebrationCategory as CelebrationCategorySchema,
    CelebrationCategoryCreate,
    CelebrationCategoryUpdate,
)


def get_celebration_categories(
    db: Session, pagination: PaginationParams,
) -> Paginated[CelebrationCategorySchema]:
    total, items = db_get_celebration_categories(
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


def get_celebration_category_by_id(category_id: int, db: Session) -> CelebrationCategorySchema:
    cat = db_get_celebration_category_by_id(category_id, db)
    if not cat:
        raise NotFoundError("CelebrationCategory")
    return cat


def create_celebration_category(
    data: CelebrationCategoryCreate, db: Session,
) -> CelebrationCategorySchema:
    category = CelebrationCategory(name=data.name, order_index=data.order_index)
    try:
        return db_create_celebration_category(category, db)
    except IntegrityError as e:
        db.rollback()
        raise AlreadyExistsError("CelebrationCategory") from e


def update_celebration_category(
    category_id: int, data: CelebrationCategoryUpdate, db: Session,
) -> CelebrationCategorySchema:
    cat = db_get_celebration_category_by_id(category_id, db)
    if not cat:
        raise NotFoundError("CelebrationCategory")
    cat.name = data.name
    cat.order_index = data.order_index
    return db_update_celebration_category(cat, db)


def delete_celebration_category(category_id: int, db: Session) -> CelebrationCategorySchema:
    cat = db_get_celebration_category_by_id(category_id, db)
    if not cat:
        raise NotFoundError("CelebrationCategory")
    return db_delete_celebration_category(cat, db)

