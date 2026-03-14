from pydantic import BaseModel, ConfigDict


class CelebrationCategoryBase(BaseModel):
    name: str | None = None
    order_index: int | None = None


class CelebrationCategoryCreate(CelebrationCategoryBase):
    pass


class CelebrationCategoryUpdate(CelebrationCategoryBase):
    pass


class CelebrationCategory(CelebrationCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

