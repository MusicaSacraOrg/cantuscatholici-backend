from pydantic import BaseModel, ConfigDict


class StaticContentRead(BaseModel):
    id: int
    content_base_id: int
    path: str

    model_config = ConfigDict(from_attributes=True)

