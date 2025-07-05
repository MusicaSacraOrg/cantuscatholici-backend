from fastapi import APIRouter

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/")
async def default():
    return {"message": "Hello from user router"}
