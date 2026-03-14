from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

import app.models
from app.common.exceptions import DomainError
from app.config import storage_settings
from app.database import SessionLocal
from app.routes.author import author_router
from app.routes.celebration import celebration_router
from app.routes.celebration_category import celebration_category_router
from app.routes.celebration_part import celebration_part_router
from app.routes.person import person_router
from app.routes.review import review_router
from app.routes.song import song_router
from app.routes.static_content import static_content_router
from app.routes.tag import tag_router
from app.routes.tag_tegory import tag_category_router
from app.routes.user import user_router
from app.routes.user_role import user_role_router
from app.services.user_role import ensure_all_exist


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
    "http://localhost:3001",
    "http://127.0.0.1:3001",
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

app.include_router(static_content_router)
app.include_router(review_router)
app.include_router(song_router)
app.include_router(tag_router)
app.include_router(tag_category_router)
app.include_router(user_router)
app.include_router(user_role_router)


@app.get("/")
async def root():
    return {"message": "Hello from Cantus Catholici!"}
