FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    git config --global init.defaultBranch main && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Create a colocated jj+git repo with some history
RUN jj git init --colocate /home/user/myrepo && \
    cd /home/user/myrepo && \
    echo "# Project" > README.md && \
    echo "def main(): pass" > app.py && \
    jj describe -m "init: project setup" && \
    jj new -m "feat: add core application" && \
    echo "def core(): return 42" > core.py && \
    jj new -m "feat: add utility functions" && \
    echo "def helper(): return True" > utils.py && \
    jj bookmark create main -r @- && \
    jj new "main" -m "wip: feature work in progress"

# Simulate a bad state: git HEAD is detached pointing to a specific commit
# (not the jj working copy parent), AND there are uncommitted changes
RUN cd /home/user/myrepo && \
    SECOND_COMMIT=$(git log --oneline | grep "feat: add core" | head -1 | awk '{print $1}') && \
    git checkout --detach "$SECOND_COMMIT" && \
    echo "# This change must be preserved" >> README.md && \
    echo "IMPORTANT_CONFIG = 'value'" > config.py

CMD ["/bin/bash"]