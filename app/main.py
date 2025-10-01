from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.calendar.router import calendar_router
from app.common.exceptions import DomainError
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


@app.exception_handler(DomainError)
async def handle_domain_error(request: Request, exc: DomainError):
    payload = {
        "type": f"https://cantuscatholici.sk/probs/{exc.code}",
        "detail": str(exc),
        "instance": str(request.url),
        **exc.extra,
    }
    return JSONResponse(
        payload,
        status_code=exc.http_status,
        media_type="application/problem+json",
        headers=exc.headers or None,
    )


ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

ORIGIN_REGEX = r"^https:\/\/([a-z0-9-]+\.)?cantuscatholici\.sk$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_origin_regex=ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
