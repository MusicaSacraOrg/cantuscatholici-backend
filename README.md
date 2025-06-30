# Cantus Catholici backend

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Developing

**Setup of development environment**:
  1. First install [uv](https://docs.astral.sh/uv/getting-started/installation/).
  2. After installation, run `uv sync`.
  3. Then run `uv run fastapi dev`.
  4. You are ready to go.

**Code linting** (code with ruff check errors will not be merged):
  1. Just run `uv run ruff check`.
  2. Fix errors, go to step 1.

**Adding dependencies**:

To add a dependency, run `uv add <your-dependency-here>`. When adding dependency, which
is required only for development, use `uv add --dev <your-dependency-here>`.

Do not forget to commit `pyproject.toml` as a commit and `uv.lock` as another one.

**Keep a changelog**:

We keep a changelog, see `CHANGELOG.md` file please.
