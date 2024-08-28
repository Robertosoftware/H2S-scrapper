precommit:
    poetry run pre-commit run --all-files

install:
    poetry install --with dev

build:
    poetry build

run:
    poetry run h2s_scrapper
