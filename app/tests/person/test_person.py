import pytest
from sqlalchemy.exc import IntegrityError

from app.person.models import Person
from app.static_content.models import StaticContent


def test_create_person(session):
    person = Person(name="John", surname="Doe", description="A test person")
    session.add(person)
    session.commit()

    assert person.id is not None
    assert person.name == "John"
    assert person.surname == "Doe"
    assert person.description == "A test person"
    assert person.avatar is None
    assert isinstance(person.id, int)


def test_create_person_with_avatar(session):
    static_content = StaticContent(path="/images/john_avatar.jpg")
    session.add(static_content)
    session.commit()

    person = Person(name="John", surname="Doe", avatar=static_content.id)
    session.add(person)
    session.commit()

    assert person.id is not None
    assert person.name == "John"
    assert person.surname == "Doe"
    assert person.avatar == static_content.id
    assert isinstance(person.id, int)


def test_get_person(session):
    person = Person(name="Jane", surname="Smith", description="Another test person")
    session.add(person)
    session.commit()

    retrieved_person = session.query(Person).filter_by(name="Jane").first()
    assert retrieved_person is not None
    assert retrieved_person.name == "Jane"
    assert retrieved_person.surname == "Smith"
    assert retrieved_person.description == "Another test person"
    assert isinstance(retrieved_person.id, int)


def test_update_person(session):
    person = Person(name="Bob", surname="Johnson")
    session.add(person)
    session.commit()

    person.name = "Alice"
    person.description = "Updated description"
    session.commit()

    updated_person = session.query(Person).filter_by(id=person.id).first()
    assert updated_person.name == "Alice"
    assert updated_person.surname == "Johnson"
    assert updated_person.description == "Updated description"


def test_delete_person(session):
    person = Person(name="Alice", surname="Johnson")
    session.add(person)
    session.commit()

    session.delete(person)
    session.commit()

    deleted_person = session.query(Person).filter_by(id=person.id).first()
    assert deleted_person is None


def test_person_required_fields(session):
    person = Person(name=None, surname="Doe")
    session.add(person)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()

    person = Person(name="John", surname=None)
    session.add(person)

    with pytest.raises(IntegrityError):
        session.commit()


def test_person_optional_fields(session):
    person = Person(name="John", surname="Doe")
    session.add(person)
    session.commit()

    assert person.description is None
    assert person.avatar is None


def test_person_avatar_foreign_key_constraint(session):
    # Person with non-existent avatar id
    person = Person(name="John", surname="Doe", avatar=999999)
    session.add(person)

    with pytest.raises(IntegrityError):
        session.commit()


def test_person_avatar_relationship(session):
    static_content = StaticContent(path="/images/profile.jpg")
    session.add(static_content)
    session.commit()

    person = Person(name="John", surname="Doe", avatar=static_content.id)
    session.add(person)
    session.commit()

    # Verify relation
    assert person.avatar == static_content.id

    # Update avatar
    new_static_content = StaticContent(path="/images/new_profile.jpg")
    session.add(new_static_content)
    session.commit()

    person.avatar = new_static_content.id
    session.commit()

    updated_person = session.query(Person).filter_by(id=person.id).first()
    # Verify relation again
    assert updated_person.avatar == new_static_content.id
