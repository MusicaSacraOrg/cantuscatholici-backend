import pytest

import alembic.command
from alembic.config import Config

pytest_plugins = [
    "app.tests.src.fixtures",
]


# TODO inefficient, need to implement it with rollback
@pytest.fixture(scope="function")
def init_schema():
    config = Config(toml_file="pyproject.toml")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")
