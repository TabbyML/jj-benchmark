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
LABEL Description="jj repo at /home/user/repo with two commits; working copy described as 'wip: add feature' to be amended."

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "# My Project" > README.md && \
    jj describe -m "chore: initial setup" && \
    jj new && \
    printf 'def hello():\n    pass\n' > feature.py && \
    jj describe -m "wip: add feature"

# Container contents:
#   - /home/user/repo — jj repository with two commits:
#       1. "chore: initial setup" (README.md)
#       2. "wip: add feature" @ (feature.py with def hello(): pass)

CMD ["/bin/bash"]
