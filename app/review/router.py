from fastapi import APIRouter

review_router = APIRouter(
    prefix="/review",
    tags=["Review"],
    responses={404: {"description": "Not found"}},
)


@review_router.get("/")
async def default():
    return {"message": "Hello from calendar router"}
