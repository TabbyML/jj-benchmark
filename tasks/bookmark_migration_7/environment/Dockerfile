FROM ubuntu:22.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip bash && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with main and feature-x bookmarks."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Developer" && \
    jj config set --repo user.email "dev@example.com" && \
    echo "main content" > file.txt && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new && \
    echo "feature content" > file.txt && \
    jj describe -m "Old feature commit" && \
    jj bookmark create feature-x && \
    jj new main && \
    echo "working copy content" > file.txt && \
    jj describe -m "Working copy commit"

# Container contents:
#   • /home/user/repo  — jj repository with:
#       - main bookmark
#       - feature-x bookmark on an older commit
#       - a working copy ahead of main

CMD ["/bin/bash"]
