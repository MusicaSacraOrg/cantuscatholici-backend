from fastapi import APIRouter

song_router = APIRouter(
    prefix="/song",
    tags=["Song"],
    responses={404: {"description": "Not found"}},
)


@song_router.get("/")
async def default():
    return {"message": "Hello from song router"}
