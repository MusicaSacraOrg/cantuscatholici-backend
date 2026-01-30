from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.content import MsczContent
from app.models.content_base import ContentBase
from app.models.static_content import StaticContent


def test_create_mscz_content(session):
    base = ContentBase(type="content_base")
    c_mscz_file = StaticContent(path="/files/file1.mscz")
    c_svg_file = StaticContent(path="/files/file1.svg")
    pdf_file = StaticContent(path="/files/file1.pdf")
    mp3_file = StaticContent(path="/files/file1.mp3")

    session.add_all([base, c_mscz_file, c_svg_file, pdf_file, mp3_file])
    session.commit()

    mscz_content = MsczContent(
        c_mscz_file_id=c_mscz_file.id,
        c_svg_file_id=c_svg_file.id,
        pdf_file_id=pdf_file.id,
        mp3_file_id=mp3_file.id,
    )
    session.add(mscz_content)
    session.commit()

    assert mscz_content.id is not None
    assert mscz_content.c_mscz_file_id == c_mscz_file.id
    assert mscz_content.c_svg_file_id == c_svg_file.id
    assert mscz_content.pdf_file_id == pdf_file.id
    assert mscz_content.mp3_file_id == mp3_file.id
    assert isinstance(mscz_content.added_at, datetime)


def test_create_mscz_content_without_optional_mp3(session):
    base = ContentBase(type="content_base")
    c_mscz_file = StaticContent(path="/files/file2.mscz")
    c_svg_file = StaticContent(path="/files/file2.svg")
    pdf_file = StaticContent(path="/files/file2.pdf")

    session.add_all([base, c_mscz_file, c_svg_file, pdf_file])
    session.commit()

    mscz_content = MsczContent(
        c_mscz_file_id=c_mscz_file.id,
        c_svg_file_id=c_svg_file.id,
        pdf_file_id=pdf_file.id,
        mp3_file_id=None,
    )
    session.add(mscz_content)
    session.commit()

    assert mscz_content.id is not None
    assert mscz_content.mp3_file_id is None


def test_required_fields(session):
    mscz_content = MsczContent()
    session.add(mscz_content)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_foreign_key_constraints(session):
    mscz_content = MsczContent(
        c_mscz_file_id=999999,
        c_svg_file_id=999999,
        pdf_file_id=999999,
        mp3_file_id=999999,
    )
    session.add(mscz_content)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
