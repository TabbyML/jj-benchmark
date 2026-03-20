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
LABEL Description="jj repo at /home/user/project; feature commit based on root() needs rebasing onto 'main' bookmark."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "print('main')" > main.py && \
    jj describe -m "chore: project setup" && \
    jj bookmark create main && \
    jj new 'root()' && \
    echo "def helper(): pass" > helper.py && \
    jj describe -m "feat: add helper"

# Container contents:
#   - /home/user/project — jj repo
#       - "chore: project setup" at bookmark 'main' (main.py)
#       - "feat: add helper" @ based on root() (helper.py) — needs rebase onto main

CMD ["/bin/bash"]
