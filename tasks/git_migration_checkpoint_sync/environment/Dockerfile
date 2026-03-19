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
LABEL Description="Colocated git and jj repository with a feature-x branch."

RUN mkdir -p /home/user/my-project && \
    cd /home/user/my-project && \
    git init && \
    git config user.name "Test User" && \
    git config user.email "test@example.com" && \
    echo "base" > base.txt && \
    git add base.txt && \
    git commit -m "Initial commit" && \
    git checkout -b feature-x && \
    echo "feature work" > feature.txt && \
    git add feature.txt && \
    git commit -m "Work on feature-x" && \
    jj git init --colocate && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    jj metaedit --update-author

# Container contents:
#   - /home/user/my-project  — Colocated git and jj repository
#       - Git branch "feature-x"
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
