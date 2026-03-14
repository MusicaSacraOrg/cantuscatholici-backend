from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    tag_category_id: int


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class Tag(TagBase):
    id: int
