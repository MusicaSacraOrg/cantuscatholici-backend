from fastapi import APIRouter
from typing import List
from ..schemas.tag import Tag as TagSchema
from ..schemas.tag import TagCreate as TagCreateSchema

from app.database import DbSessionDep

from ..services.tag import (
    get_tags,
    get_tags_by_category,
    update_tag,
    create_tag,
    delete_tag,
    get_tag_by_id
)

tag_router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get("/", response_model=List[TagSchema])
async def get_tags_endpoint(db: DbSessionDep):
    return {"items": get_tags(db)}


@tag_router.get("/{tag_id}", response_model=TagSchema)
async def get_tag_by_id_endpoint(tag_id: int, db: DbSessionDep):
    return {"tag": get_tag_by_id(tag_id, db)}


@tag_router.get("/{category_tag_id}", response_model=List[TagSchema])
async def get_tags_by_category_id_endpoint(category_tag_id: int, db: DbSessionDep):
    return {"items": get_tags_by_category(category_tag_id, db)}


@tag_router.post("/create", response_model=TagSchema)
async def create_tag_endpoint(tag: TagCreateSchema, db: DbSessionDep):
    return {"tag": create_tag(tag, db)}
    # try:
     #   return create_tag(tag, db)
    #except Exception as e:
        # TODO there should not be an exception
        # TODO raise http error
     #   raise e


@tag_router.put("/update/{tag_id}", response_model=TagSchema)
def update_tag_endpoint(tag_id: int, tag: TagCreateSchema, db: DbSessionDep):
    return {"tag": update_tag(tag_id, tag, db)}
    # try:
    #    return update_tag(db, tag_id, tag_in)
    #except TagNotFoundError:
     #   raise HTTPException(status_code=404, detail="Tag not found")
    #except TagAlreadyExistsError as e:
     #   raise HTTPException(status_code=409, detail=str(e))


@tag_router.delete("/delete/{tag_id}", response_model=TagSchema)
def delete_tag_endpoint(tag_id: int, db: DbSessionDep):
    return {"tag": delete_tag(tag_id, db)}