from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.calendar.router import calendar_router
from app.database import SessionLocal
from app.review.router import review_router
from app.song.router import song_router
from app.static_content.router import static_content_router
from app.tag.router import tag_router
from app.user.router import user_router
from app.user_role.router import user_role_router
from app.user_role.service import ensure_all_exist


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    # ensure all predefined user roles exist
    with SessionLocal() as db:
        ensure_all_exist(db)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(calendar_router)
app.include_router(static_content_router)
app.include_router(review_router)
app.include_router(song_router)
app.include_router(tag_router)
app.include_router(user_router)
app.include_router(user_role_router)


@app.get("/")
async def root():
    return {"message": "Hello from cantus catholici!"}
