from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginationParams(BaseModel):
    limit: PositiveInt
    offset: NonNegativeInt


async def pagination_params(
    limit: int = Query(10, ge=1, le=100, description="Max number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)


PaginationParamsDep = Annotated[PaginationParams, Depends(pagination_params)]
