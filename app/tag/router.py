from fastapi import APIRouter

tag_router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get("/")
async def default():
    return {"message": "Hello from tag router"}
