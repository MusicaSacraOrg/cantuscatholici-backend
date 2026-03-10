import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.calendar import service
from app.common.deps.auth import require_role
from app.database import DbSessionDep
from app.user.schema import UserInDb
from app.user_role.service import PredefinedUserRoles

calendar_router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"],
    responses={404: {"description": "Not found"}},
)


class CalendarEntryCreate(BaseModel):
    api_id: str
    title: str | None = None
    description: str | None = None
    date: datetime.date | None = None
    feast_type: str | None = None
    liturgical_season: str | None = None
    is_recurring: bool = False


class CalendarEntryUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    date: datetime.date | None = None
    feast_type: str | None = None
    liturgical_season: str | None = None


@calendar_router.get("/")
def get_calendar(
    session: DbSessionDep,
    year: int | None = Query(default=None),
    month: int | None = Query(default=None),
    season: str | None = Query(default=None),
):
    return service.get_entries(session, year=year, month=month, season=season)


@calendar_router.get("/today")
def get_today(session: DbSessionDep):
    return service.get_today(session)


@calendar_router.get("/feasts")
def get_feasts(session: DbSessionDep):
    return service.get_feasts(session)


@calendar_router.get("/song/{song_id}")
def get_song_calendar(session: DbSessionDep, song_id: int):
    return service.get_entries_for_song(session, song_id)


_require_redactor = require_role(PredefinedUserRoles.REDACTOR, PredefinedUserRoles.ADMIN)


@calendar_router.post("/")
def create_entry(
    session: DbSessionDep,
    body: CalendarEntryCreate,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.create_entry(
        session,
        api_id=body.api_id,
        title=body.title,
        description=body.description,
        entry_date=body.date,
        feast_type=body.feast_type,
        liturgical_season=body.liturgical_season,
        is_recurring=body.is_recurring,
    )


@calendar_router.put("/{entry_id}")
def update_entry(
    session: DbSessionDep,
    entry_id: int,
    body: CalendarEntryUpdate,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.update_entry(
        session,
        entry_id=entry_id,
        title=body.title,
        description=body.description,
        entry_date=body.date,
        feast_type=body.feast_type,
        liturgical_season=body.liturgical_season,
    )


@calendar_router.post("/{entry_id}/songs/{song_id}")
def add_song(
    session: DbSessionDep,
    entry_id: int,
    song_id: int,
    _current_user: Annotated[UserInDb, Depends(_require_redactor)],
):
    return service.add_song_to_entry(session, entry_id, song_id)
