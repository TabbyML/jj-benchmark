FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="jj repository environment with main and feature-branch bookmarks containing a conflict in data.txt."

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init --colocate && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    echo "Base content" > data.txt && \
    jj commit -m "base" && \
    echo "Line from main" > data.txt && \
    jj commit -m "main commit" && \
    jj bookmark create main -r @- && \
    jj new @-- -m "feature commit 1" && \
    echo "Line from feature" > data.txt && \
    jj commit -m "feature commit 1" && \
    jj new @- -m "feature commit 2" && \
    echo "Another file" > other.txt && \
    jj commit -m "feature commit 2" && \
    jj bookmark create feature-branch -r @- && \
    jj new feature-branch

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/repo - jj repository with base, main, and feature-branch commits
#   - Conflicting changes in data.txt between main and feature-branch

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]