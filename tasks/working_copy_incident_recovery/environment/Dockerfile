FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo recovering working copy edits after an incident."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    mkdir -p config scripts data && \
    echo "initial settings" > config/settings.yaml && \
    echo "echo 'deploying'" > scripts/deploy.sh && \
    echo "binary cache data" > data/cache.bin && \
    jj describe -m "chore: initial setup" && \
    jj new && \
    echo "updated settings for incident" > config/settings.yaml && \
    echo "echo 'deploying... error'" > scripts/deploy.sh && \
    rm data/cache.bin && \
    jj describe -m "wip: working on settings and deploy"

# Container contents:
#   - /home/user/repo - jj repository with an initial commit and a working copy containing uncommitted modifications to settings.yaml, deploy.sh, and a deleted cache.bin file.

CMD ["/bin/bash"]
