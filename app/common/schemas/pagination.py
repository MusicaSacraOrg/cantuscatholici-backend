from typing import TypeVar

from pydantic import BaseModel, NonNegativeInt, PositiveInt

T = TypeVar("T")


class Paginated[T](BaseModel):
    total: NonNegativeInt
    limit: PositiveInt
    offset: NonNegativeInt
    items: list[T]
