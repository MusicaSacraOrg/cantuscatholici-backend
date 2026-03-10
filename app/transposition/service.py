import json
import logging
import os
import shutil
import subprocess
import tempfile
import zipfile
from io import BytesIO

from sqlalchemy.orm import Session

from app.content.models import MsczContent
from app.song.exceptions import SongNotFoundException
from app.song.models import Song
from app.static_content.service import get_file, store_file

logger = logging.getLogger(__name__)

TRANSPOSE_TIMEOUT = int(os.getenv("TRANSPOSE_TIMEOUT", "60"))


def _resolve_musescore_bin() -> str | None:
    # Prefer explicit versioned binary names, then generic aliases.
    for binary in ("musescore4", "musescore", "mscore"):
        found = shutil.which(binary)
        if found:
            return found
    return None


def _build_transpose_options(semitones: int) -> str:
    return json.dumps(
        {
            "mode": "by_interval",
            "direction": "up" if semitones > 0 else "down",
            "transposeInterval": abs(semitones),
            "transposeKeySignatures": True,
            "transposeChordNames": True,
            "useDoubleSharpsFlats": False,
        },
        separators=(",", ":"),
    )


def transpose_mscz(session: Session, song_id: int, semitones: int) -> dict:
    # 1. Validation Logic
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

    musescore_bin = _resolve_musescore_bin()
    xvfb_bin = shutil.which("xvfb-run")

    def with_display(cmd: list[str]) -> list[str]:
        return [xvfb_bin, "-a", *cmd] if xvfb_bin else cmd

    if not musescore_bin:
        return {"error": "MuseScore binary not found on server.", "available": False}

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mscz")
        output_mscz = os.path.join(tmpdir, "output.mscz")

        # Write the binary data to a temp file
        with open(input_path, "wb") as f:
            f.write(mscz_data)
            f.flush() # Ensure data is written to disk

        # 2. Build the Command
        # We use xvfb-run to provide a virtual display for headless servers
        transpose_options = _build_transpose_options(semitones)
        cmd = with_display(
            [
                musescore_bin,
                input_path,
                "-o",
                output_mscz,
                "--transpose",
                transpose_options,
            ],
        )

        try:
            # 3. Execution
            subprocess.run(
                cmd,
                timeout=TRANSPOSE_TIMEOUT,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"MuseScore Error: {e.stderr}")
            return {
                "error": f"Transposition failed: {e.stderr[:200]}",
                "available": False,
            }
        except subprocess.TimeoutExpired:
            return {"error": "Transposition timed out", "available": False}

        # 4. Exporting Other Formats
        # Note: In MuseScore 4, you can often do multiple exports in one go
        # using a json job file, but separate calls are safer for debugging.
        formats = {
            "mscz": output_mscz,
            "svg": os.path.join(tmpdir, "output.svg"),
            "pdf": os.path.join(tmpdir, "output.pdf"),
        }
        results = {}

        for fmt, path in formats.items():
            if fmt != "mscz": # Generate SVG/PDF from the ALREADY transposed MSCZ
                conv_cmd = with_display([musescore_bin, output_mscz, "-o", path])
                try:
                    subprocess.run(
                        conv_cmd,
                        timeout=TRANSPOSE_TIMEOUT,
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                except subprocess.CalledProcessError as e:
                    logger.error(f"MuseScore {fmt.upper()} export error: {e.stderr}")
                    return {
                        "error": f"Failed to export {fmt}: {e.stderr[:200]}",
                        "available": False,
                    }
                except subprocess.TimeoutExpired:
                    return {"error": f"Export to {fmt} timed out", "available": False}

            # MuseScore can emit paginated SVGs like output-1.svg/output-2.svg
            if fmt == "svg" and not os.path.exists(path):
                svg_candidates = sorted(
                    [
                        os.path.join(tmpdir, name)
                        for name in os.listdir(tmpdir)
                        if name.startswith("output-") and name.endswith(".svg")
                    ],
                )
                if svg_candidates:
                    path = svg_candidates[0]

            if os.path.exists(path):
                with open(path, "rb") as f:
                    stored = store_file(session, f"trans_{semitones}.{fmt}", f.read())
                    results[fmt] = stored

        # 5. Database Update
        if all(k in results for k in ["mscz", "svg", "pdf"]):
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
