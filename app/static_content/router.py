from fastapi import APIRouter

static_content_router = APIRouter(
    prefix="/static_content",
    tags=["Content"],
    responses={404: {"description": "Not found"}},
)


@static_content_router.get("/")
async def default():
    return {"message": "Hello from static_content router"}
