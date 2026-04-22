FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Jujutsu repository initialized at /home/user/repo"

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj config set --user user.name "Your Name" && \
    jj config set --user user.email "your@email.com" && \
    jj git init

# Container contents:
#   - jj installed
#   - /home/user/repo - initialized jj repository

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
