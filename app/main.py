from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import app.models
from app.calendar.router import calendar_router
from app.common.exceptions import DomainError
from app.content.router import content_router
from app.database import SessionLocal
from app.person.router import person_router
from app.review.router import review_router
from app.song.router import song_router
from app.static_content.router import static_content_router
from app.tag.router import tag_router
from app.transposition.router import transposition_router
from app.tag_category.router import tag_category_router
from app.user.router import user_router
from app.user_content.router import user_content_router
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
    "http://localhost:3001",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
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


api_router = APIRouter(prefix="/api")
api_router.include_router(calendar_router)
api_router.include_router(content_router)
api_router.include_router(person_router)
api_router.include_router(static_content_router)
api_router.include_router(review_router)
api_router.include_router(song_router)
api_router.include_router(tag_router)
api_router.include_router(tag_category_router)
api_router.include_router(transposition_router)
api_router.include_router(user_router)
api_router.include_router(user_content_router)
api_router.include_router(user_role_router)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello from cantus catholici!"}
