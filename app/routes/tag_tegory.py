from fastapi import APIRouter, Depends

from ..auth.permissions import required_role
from ..common.deps.pagination import PaginationParamsDep
from ..database import DbSessionDep
from ..schemas.tag_category import TagCategory as TagCategorySchema
from ..schemas.tag_category import TagCategoryCreate as TagCategoryCreateSchema

from app.common.schemas.pagination import Paginated
from ..services.tag_category import get_tag_categories, get_tag_category_by_id, create_tag_category, \
    update_tag_category, delete_tag_category

tag_category_router = APIRouter(
    prefix="/tag-category",
    tags=["Tag Category"],
    responses={404: {"description": "Not found"}},
)

@tag_category_router.get("/", response_model=Paginated[TagCategorySchema])
async def get_tag_categories_endpoint(db: DbSessionDep, pagination: PaginationParamsDep):
    return get_tag_categories(db, pagination)


@tag_category_router.get("/{tag_category_id}", response_model=TagCategorySchema)
async def get_tag_category_by_id_endpoint(tag_category_id: int, db: DbSessionDep):
    return {"tag_category": get_tag_category_by_id(tag_category_id, db)}


@tag_category_router.post("/create", response_model=TagCategorySchema)
async def create_tag_category_endpoint(tag_category: TagCategoryCreateSchema, db: DbSessionDep, _user = Depends(required_role("Admin"))):
    return {"tag_category": create_tag_category(tag_category, db)}


@tag_category_router.put("/update/{tag_id}", response_model=TagCategorySchema)
def update_tag_category_endpoint(tag_category_id: int, tag: TagCategoryCreateSchema, db: DbSessionDep, _user = Depends(required_role("Admin"))):
    return {"tag_category": update_tag_category(tag_category_id, tag, db)}


@tag_category_router.delete("/delete/{tag_id}", response_model=TagCategorySchema)
def delete_tag_category_endpoint(tag_category_id: int, db: DbSessionDep, _user = Depends(required_role("Admin"))):
    return {"tag_category": delete_tag_category(tag_category_id, db)}