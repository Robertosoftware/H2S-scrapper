FROM mcr.microsoft.com/devcontainers/base:alpine3.20

# Set environment variables
ENV GIT_PYTHON_REFRESH=quiet \
    TZ=Europe/Amsterdam \
    PYTHON_VERSION=3.10.12 \
    HOME="/home/vscode" \
    PYENV_ROOT="/home/vscode/.pyenv" \
    PIPX_HOME="/home/vscode/.pipx" \
    PIPX_BIN_DIR="/home/vscode/.local/bin" \
    PATH="/home/vscode/.pyenv/shims:/home/vscode/.pyenv/bin:/home/vscode/.local/bin:$PATH" \
    VIRTUAL_ENV_DISABLE_PROMPT=1

# Install just
RUN wget https://github.com/casey/just/releases/download/1.25.2/just-1.25.2-aarch64-unknown-linux-musl.tar.gz && \
    tar -xvf just-1.25.2-aarch64-unknown-linux-musl.tar.gz -C /usr/bin && \
    rm just-1.25.2-aarch64-unknown-linux-musl.tar.gz

# Update apk repositories and install prerequisites
RUN apk update &&\
    apk add git curl sqlite-dev libffi pipx gcc python3-dev musl-dev linux-headers  && \
    rm -rf /var/lib/apt/lists/*

# Install pyenv and python
RUN curl https://pyenv.run | bash && \
    pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    pyenv rehash

# Install pipx and poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pipx && \
    pipx ensurepath && \
    pipx install poetry

# Add poetry-git-version-plugin
RUN poetry self add poetry-git-version-plugin

# Configure poetry to create virtualenvs in the project directory
RUN poetry config virtualenvs.in-project true

# Add sudo permissions for the vscode user
RUN adduser vscode wheel && \
    echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Ensure permissions are set correctly
RUN sudo chmod -R 777 /home/vscode
