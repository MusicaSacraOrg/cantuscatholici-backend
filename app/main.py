from fastapi import FastAPI

from app.calendar.router import calendar_router
from app.content.router import content_router
from app.review.router import review_router
from app.song.router import song_router
from app.tag.router import tag_router
from app.user.router import user_router

app = FastAPI()

app.include_router(calendar_router)
app.include_router(content_router)
app.include_router(review_router)
app.include_router(song_router)
app.include_router(tag_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello from cantus catholici!"}
