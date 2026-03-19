FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL description="jj task: rebase stacked service patches onto updated infra/base and verify bookmark tracking"

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
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV JJ_USER="Platform Engineer"
ENV JJ_EMAIL="platform@example.com"
ENV EDITOR=true

WORKDIR /home/user

RUN mkdir -p /home/user/monorepo \
    && cd /home/user/monorepo \
    && jj git init --colocate \
    && jj config set --repo user.name "Platform Engineer" \
    && jj config set --repo user.email "platform@example.com" \
    && echo "# monorepo entrypoint" > scaffold.py \
    && jj describe -m "chore: initial monorepo scaffold" \
    && COMMIT_A=$(jj log -r @ --no-graph -T 'change_id.short(8)') \
    && jj new \
    && mkdir -p lib \
    && echo "# shared config helper" > lib/config.py \
    && jj describe -m "feat: add shared config helper" \
    && jj new \
    && echo "# health check module" > lib/health.py \
    && jj describe -m "feat: add health check module" \
    && jj bookmark create infra/base -r @ \
    && jj edit "$COMMIT_A" \
    && jj new \
    && mkdir -p services \
    && echo "# auth token validation patch" > services/auth.py \
    && jj describe -m "fix: patch auth token validation" \
    && jj bookmark create services/auth-patch -r @ \
    && jj edit "$COMMIT_A" \
    && jj new \
    && mkdir -p services \
    && echo "# cache TTL enforcement patch" > services/cache.py \
    && jj describe -m "fix: add cache TTL enforcement" \
    && jj bookmark create services/cache-patch -r @ \
    && jj new infra/base

CMD ["/bin/bash"]
