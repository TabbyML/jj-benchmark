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
LABEL Description="jj repo with a linear stack of commits (A -> B -> C) in /home/user/repo."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "A" > a.txt && \
    jj commit -m "A" && \
    echo "B" > b.txt && \
    jj commit -m "B" && \
    echo "C" > c.txt && \
    jj commit -m "C"

# Container contents:
#   - /home/user/repo  — jj repository with linear history: A -> B -> C -> @(empty)
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
