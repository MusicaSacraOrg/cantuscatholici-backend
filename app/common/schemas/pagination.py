from typing import TypeVar, Literal

from pydantic import BaseModel, NonNegativeInt, PositiveInt

T = TypeVar("T")


class Paginated[T](BaseModel):
    total: NonNegativeInt
    limit: PositiveInt
    offset: NonNegativeInt
    order_by: str | None = None
    order: Literal["asc", "desc"] = "asc"
    items: list[T]
