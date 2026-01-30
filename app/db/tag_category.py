from sqlalchemy.orm import Session

from ..models.tag_category import TagCategory
from ..schemas.tag_category import TagCategory as TagCategorySchema


def db_get_tags_categories(db: Session):
    tag_categories = db.query(TagCategory).all()

    if not tag_categories:
        return None

    return tag_categories


def db_get_tag_category(tag_category_id: int, db: Session):
    tag_category = db.query(TagCategory).filter(TagCategory.id == tag_category_id).first()

    if not tag_category:
        return None

    return tag_category


def db_create_tag_category(tag_category: TagCategorySchema, db: Session):
    tag_category = TagCategory(
        name=tag_category.name,
    )

    db.add(tag_category)
    db.commit()
    db.refresh(tag_category)

    return tag_category


def db_update_tag_category(tag_category_id, tag_category: TagCategorySchema, db: Session):
    existing_tag_category = db.query(TagCategory).filter(TagCategory.id == tag_category_id).first()

    if not existing_tag_category:
        return None

    existing_tag_category.name = tag_category.name

    db.commit()
    db.refresh(existing_tag_category)

    return existing_tag_category


def db_delete_tag_category(tag_category_id: int, db: Session):
    tag_category = db.query(TagCategory).filter(TagCategory.id == tag_category_id).first()

    if not tag_category:
        return False

    db.delete(tag_category)
    db.commit()

    return True