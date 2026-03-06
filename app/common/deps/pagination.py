from typing import Annotated, Literal

from fastapi import Depends, Query
from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginationParams(BaseModel):
    limit: PositiveInt | None
    offset: NonNegativeInt
    order_by: str | None = None
    order: Literal["asc", "desc"] = "asc"


async def pagination_params(
    limit: int | None = Query(
        None,
        ge=1,
        le=100,
        description="Max number of items to return",
    ),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    order_by: str | None = Query(None, description="Order by"),
    order: Literal["asc", "desc"] = Query(None, description="Order asc or desc"),
) -> PaginationParams:
    return PaginationParams(
        limit=limit,
        offset=offset,
        order=order,
        order_by=order_by,
    )


PaginationParamsDep = Annotated[PaginationParams, Depends(pagination_params)]
