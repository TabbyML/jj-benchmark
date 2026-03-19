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
LABEL Description="jj repo with an initial commit, an abandoned feature commit, and a new commit on main."

RUN mkdir -p /home/user/workspace && \
    jj git init /home/user/workspace/auth-service && \
    cd /home/user/workspace/auth-service && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "# Auth Service" > README.md && \
    jj describe -m "Initial commit" && \
    jj bookmark create -r @ main && \
    jj new main -m "Add login feature" && \
    echo "def login(): pass" > login.py && \
    jj bookmark create -r @ feature-login && \
    jj bookmark forget feature-login && \
    jj abandon && \
    jj new main -m "Add utils" && \
    echo "def util(): pass" > utils.py

# Container contents:
#   - /home/user/workspace/auth-service — jj repository with:
#       - 'main' branch pointing to "Initial commit"
#       - An abandoned commit "Add login feature" with file login.py
#       - A new child commit "Add utils" with file utils.py
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
