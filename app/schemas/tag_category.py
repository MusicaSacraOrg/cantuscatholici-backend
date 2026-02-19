from pydantic import BaseModel


class TagCategoryBase(BaseModel):
    name: str


class TagCategory(TagCategoryBase):
    id: int


class TagCategoryCreate(TagCategoryBase):
    pass