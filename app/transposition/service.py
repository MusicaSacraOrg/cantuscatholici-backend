import os
import shutil
import subprocess
import tempfile

from sqlalchemy.orm import Session

from app.content.models import MsczContent
from app.song.exceptions import SongNotFoundException
from app.song.models import Song
from app.static_content.service import store_file

MUSESCORE_BIN = shutil.which("musescore4") or shutil.which("mscore") or "musescore4"
TRANSPOSE_TIMEOUT = 60  # seconds


def _find_cached(
    session: Session, original_mscz_id: int, semitones: int,
) -> MsczContent | None:
    """Check if a transposed version already exists (by convention: same parent)."""
    # For now, no caching — always regenerate
    return None


def transpose_mscz(
    session: Session, song_id: int, semitones: int,
) -> dict:
    """Transpose a song's MuseScore file by the given number of semitones."""
    song = session.get(Song, song_id)
    if song is None:
        raise SongNotFoundException("Song not found")
    if not song.mscz_id:
        raise SongNotFoundException("Song has no MuseScore content")

    mscz = session.get(MsczContent, song.mscz_id)
    if mscz is None:
        raise SongNotFoundException("MuseScore content not found")

    from app.static_content.service import get_file

    mscz_data, _ = get_file(session, mscz.c_mscz_file_id)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mscz")
        output_mscz = os.path.join(tmpdir, "output.mscz")
        output_svg = os.path.join(tmpdir, "output.svg")
        output_pdf = os.path.join(tmpdir, "output.pdf")

        with open(input_path, "wb") as f:
            f.write(mscz_data)

        # Transpose using MuseScore CLI
        try:
            subprocess.run(
                [
                    MUSESCORE_BIN,
                    input_path,
                    "--transpose", str(semitones),
                    "-o", output_mscz,
                ],
                timeout=TRANSPOSE_TIMEOUT,
                check=True,
                capture_output=True,
            )
        except FileNotFoundError:
            return {
                "error": "MuseScore CLI not found. Install musescore4 on the server.",
                "available": False,
            }
        except subprocess.CalledProcessError as e:
            return {
                "error": f"MuseScore transposition failed: {e.stderr.decode()[:200]}",
                "available": False,
            }

        # Export SVG and PDF
        for output, fmt in [(output_svg, "svg"), (output_pdf, "pdf")]:
            try:
                subprocess.run(
                    [MUSESCORE_BIN, output_mscz, "-o", output],
                    timeout=TRANSPOSE_TIMEOUT,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                pass

        # Store files
        results = {}
        for path, name_suffix in [
            (output_mscz, "mscz"),
            (output_svg, "svg"),
            (output_pdf, "pdf"),
        ]:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    data = f.read()
                stored = store_file(session, f"transposed_{semitones}.{name_suffix}", data)
                results[name_suffix] = stored

        if "mscz" in results and "svg" in results and "pdf" in results:
            new_mscz = MsczContent(
                c_mscz_file_id=results["mscz"]["id"],
                c_svg_file_id=results["svg"]["id"],
                pdf_file_id=results["pdf"]["id"],
            )
            session.add(new_mscz)
            session.commit()

            return {
                "available": True,
                "mscz_content_id": new_mscz.id,
                "svg_url": f"/api/static_content/{results['svg']['id']}",
                "pdf_url": f"/api/static_content/{results['pdf']['id']}",
            }

    return {"error": "Transposition produced no output files", "available": False}


def get_transpositions(session: Session, song_id: int) -> list[dict]:
    """List cached transpositions for a song (placeholder for future caching)."""
    return []
