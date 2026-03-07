FROM ubuntu:22.04

LABEL Author="jj-task-builder"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV HOME=/home/user
ENV JJ_USER="Test User"
ENV JJ_EMAIL="test@example.com"
ENV EDITOR=true

RUN mkdir -p /home/user/.config/jj

RUN mkdir -p /home/user/myrepo && \
    cd /home/user/myrepo && \
    jj git init --colocate && \
    echo "Initial project setup" > README.md && \
    jj describe -m "initial commit: add README" && \
    jj new && \
    echo "# My Project" > README.md && \
    echo "" >> README.md && \
    echo "A sample project for jj onboarding." >> README.md && \
    jj describe -m "docs: expand README with project description" && \
    jj new && \
    echo "src/" > .gitignore && \
    echo "*.log" >> .gitignore && \
    jj describe -m "chore: add .gitignore" && \
    jj new && \
    echo 'version = "0.1.0"' > pyproject.toml && \
    jj describe -m "feat: add pyproject.toml" && \
    jj new && \
    echo "# Changelog" > CHANGELOG.md && \
    echo "" >> CHANGELOG.md && \
    echo "## Unreleased" >> CHANGELOG.md && \
    jj describe -m "docs: add CHANGELOG"

CMD ["/bin/bash"]
