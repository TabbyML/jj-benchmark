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
    && echo '#!/bin/bash' > scaffold.sh \
    && echo 'echo "scaffold"' >> scaffold.sh \
    && jj describe -m "chore: initial project scaffold" \
    && COMMIT_A=$(jj log -r @ --no-graph -T 'change_id.short(8)') \
    && jj bookmark create main -r @ \
    && jj new \
    && echo '#!/bin/bash' > deploy.sh \
    && echo 'echo "deploy"' >> deploy.sh \
    && jj describe -m "chore: add deploy.sh for CI pipeline" \
    && jj bookmark set main -r @ \
    && jj edit "$COMMIT_A" \
    && jj new \
    && mkdir -p metrics \
    && echo "# metrics module" > metrics/module.py \
    && jj describe -m "feat: scaffold metrics module" \
    && jj bookmark create feature/add-metrics -r @ \
    && jj new \
    && echo "# dashboard" > metrics/dashboard.py \
    && jj describe -m "feat: add metrics dashboard endpoint" \
    && jj bookmark set feature/add-metrics -r @ \
    && jj new main

CMD ["/bin/bash"]
