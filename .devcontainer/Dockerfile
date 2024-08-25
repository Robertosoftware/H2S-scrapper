FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ENV GIT_PYTHON_REFRESH=quiet
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam
ENV PYTHON_VERSION=3.10.12
ENV HOME="/home/vscode"
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PIPX_HOME="/home/vscode/.pipx"
ENV PIPX_DEFAULT_PYTHON="/home/vscode/.pyenv/shims/python"

# Install just
RUN wget https://github.com/casey/just/releases/download/1.25.2/just-1.25.2-aarch64-unknown-linux-musl.tar.gz && \
    tar -xvf just-1.25.2-aarch64-unknown-linux-musl.tar.gz -C /usr/bin && \
    rm just-1.25.2-aarch64-unknown-linux-musl.tar.gz

# Prerequisites for pyenv, poetry etc.
RUN apt-get update && \
    apt-get -y install libsqlite3-dev libffi-dev pipx gcc musl-dev python3-dev libbz2-dev openjdk-8-jdk && \
    rm -rf /var/lib/apt/lists/*

# Install pyenv
RUN curl https://pyenv.run | bash

ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN echo 'eval "$(pyenv init -)"' >>/home/vscode/.bashrc && \
    pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    pyenv rehash && \
    pip install --no-cache-dir --upgrade pip

# Poetry
RUN pipx install poetry

# pipx distros
ENV PATH="/home/vscode/.local/bin:$PATH"

# Versioning with poetry
RUN poetry self add poetry-git-version-plugin

# Create .venv in project
RUN poetry config virtualenvs.in-project true

RUN usermod -aG sudo vscode
RUN sudo chmod -R 777 /home/vscode
