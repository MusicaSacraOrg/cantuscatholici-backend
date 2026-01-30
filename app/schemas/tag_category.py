from pydantic import BaseModel


class TagCategory(BaseModel):
    name: str
    # color: str