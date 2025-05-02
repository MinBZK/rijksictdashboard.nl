set -e

poetry run ruff check app common etl tests
poetry run ruff format --check
poetry run ruff check --select I --fix

poetry run pyright app
poetry run pyright common
poetry run pyright etl
