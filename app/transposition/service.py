import logging
import zipfile
from io import BytesIO

import httpx
from sqlalchemy.orm import Session

from app.config import transposition_settings
from app.content.models import MsczContent
from app.song.exceptions import SongNotFoundException
from app.song.models import Song
from app.static_content.service import get_file, store_file

logger = logging.getLogger(__name__)

TRANSPOSE_TIMEOUT = 120  # HTTP request timeout (seconds)


def transpose_mscz(session: Session, song_id: int, semitones: int) -> dict:
    # 1. Validation / DB lookup
    song = session.get(Song, song_id)
    if not song or not song.mscz_id:
        raise SongNotFoundException("Song or MuseScore content missing")

    mscz = session.get(MsczContent, song.mscz_id)
    if not mscz:
        raise SongNotFoundException("Song or MuseScore content missing")

    mscz_data, _ = get_file(session, mscz.c_mscz_file_id)
    if not zipfile.is_zipfile(BytesIO(mscz_data)):
        return {
            "error": "Uploaded MSCZ file is invalid and cannot be transposed.",
            "available": False,
        }

    # 2. Call transposition microservice
    service_url = transposition_settings.service_url.rstrip("/")
    try:
        response = httpx.post(
            f"{service_url}/transpose",
            files={"file": ("input.mscz", mscz_data, "application/octet-stream")},
            data={"semitones": str(semitones)},
            timeout=TRANSPOSE_TIMEOUT,
        )
    except httpx.ConnectError:
        logger.error("Cannot connect to transposition service at %s", service_url)
        return {"error": "Transposition service unavailable.", "available": False}
    except httpx.TimeoutException:
        return {"error": "Transposition timed out.", "available": False}

    if response.status_code != 200:
        detail = response.text[:200]
        logger.error("Transposition service error (%d): %s", response.status_code, detail)
        return {"error": f"Transposition failed: {detail}", "available": False}

    # 3. Unzip response and store files
    try:
        zip_data = BytesIO(response.content)
        with zipfile.ZipFile(zip_data) as zf:
            results = {}
            for fmt in ("mscz", "svg", "pdf"):
                filename = f"output.{fmt}"
                file_bytes = zf.read(filename)
                stored = store_file(session, f"trans_{semitones}.{fmt}", file_bytes)
                results[fmt] = stored
    except (zipfile.BadZipFile, KeyError) as e:
        logger.error("Invalid response from transposition service: %s", e)
        return {"error": "Invalid response from transposition service.", "available": False}

    # 4. Database update
    if all(k in results for k in ("mscz", "svg", "pdf")):
        new_content = MsczContent(
            c_mscz_file_id=results["mscz"]["id"],
            c_svg_file_id=results["svg"]["id"],
            pdf_file_id=results["pdf"]["id"],
        )
        session.add(new_content)
        session.commit()
        return {
            "available": True,
            "mscz_content_id": new_content.id,
            "svg_url": f"/api/static_content/{results['svg']['id']}",
            "pdf_url": f"/api/static_content/{results['pdf']['id']}",
        }

    return {"error": "Failed to generate all required files", "available": False}


def get_transpositions(_session: Session, _song_id: int) -> list[dict]:
    """List cached transpositions for a song (placeholder for future caching)."""
    return []
