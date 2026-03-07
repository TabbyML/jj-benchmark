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
LABEL Description="jj repo with three feature bookmarks for multi-parent octopus merge task in /home/user/project."

RUN jj git init /home/user/project && \
    cd /home/user/project && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "base" > base.txt && \
    jj describe -m "base commit" && \
    jj bookmark create base && \
    jj new base && \
    echo "a" > a.txt && \
    jj describe -m "add a.txt" && \
    jj bookmark create feature-a && \
    jj new base && \
    echo "b" > b.txt && \
    jj describe -m "add b.txt" && \
    jj bookmark create feature-b && \
    jj new base && \
    echo "c" > c.txt && \
    jj describe -m "add c.txt" && \
    jj bookmark create feature-c && \
    jj new base

# Container contents:
#   - /home/user/project  — jj repository with:
#       - "base commit"
#       - "add a.txt" with bookmark feature-a
#       - "add b.txt" with bookmark feature-b
#       - "add c.txt" with bookmark feature-c
#       - A working copy based off the base commit
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]