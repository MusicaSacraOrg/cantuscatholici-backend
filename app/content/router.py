from fastapi import APIRouter

content_router = APIRouter(
    prefix="/content",
    tags=["Content"],
    responses={404: {"description": "Not found"}},
)


@content_router.get("/")
async def default():
    return {"message": "Hello from content router"}
