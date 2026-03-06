from fastapi import APIRouter

calendar_router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"],
    responses={404: {"description": "Not found"}},
)


@calendar_router.get("/")
async def default():
    return {"message": "Hello from calendar router"}
