# Cantus Catholici backend

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Developing

Developing the app is solved using **docker compose**. Just run:
  1. `docker compose up --watch`.
  2. When you are done, press `Ctrl+C` or `docker compose down`.

Changes in application are automatically reflected in docker container. However, code linting
and type checking is not integrated.

**Setup of development environment**:
  1. First install [uv](https://docs.astral.sh/uv/getting-started/installation/).
  2. After installation, run `uv sync`.

**Code linting** (code with ruff check errors will not be merged):
  1. Just run `uv run ruff check`.
  2. Fix errors, go to step 1.

**Type checking** (code with pyright errors will not be merged):
  1. Run `uv run pyright ./`.
  2. Fix errors, go to step 1.

You are ready to create merge request.

**Type checking**


**Adding dependencies**:

To add a dependency, run `uv add <your-dependency-here>`. When adding dependency, which
is required only for development, use `uv add --dev <your-dependency-here>`.

Do not forget to commit `pyproject.toml` as a commit and `uv.lock` as another one.

**Keep a changelog**:

We keep a changelog, see `CHANGELOG.md` file please.
