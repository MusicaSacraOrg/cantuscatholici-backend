from pydantic import BaseModel, ConfigDict


class CelebrationPartBase(BaseModel):
    name: str | None = None
    order_index: int | None = None


class CelebrationPartCreate(CelebrationPartBase):
    pass


class CelebrationPartUpdate(CelebrationPartBase):
    pass


class CelebrationPart(CelebrationPartBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

