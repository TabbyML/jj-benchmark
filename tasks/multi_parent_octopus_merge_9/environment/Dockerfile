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
LABEL Description="jj repo with a base commit in /home/user/octopus_repo."

RUN jj git init /home/user/octopus_repo && \
    cd /home/user/octopus_repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "base content" > base.txt && \
    jj describe -m "base"

# Container contents:
#   - /home/user/octopus_repo  — jj repository with a base commit containing base.txt
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]