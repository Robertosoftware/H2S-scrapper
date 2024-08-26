precommit:
    pre-commit run --all-files

install:
    poetry install --with dev

build:
    poetry build
