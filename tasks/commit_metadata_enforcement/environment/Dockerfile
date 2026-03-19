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
LABEL Description="jj repository configured for commit metadata enforcement"

RUN cd /home/user && \
    mkdir -p repo && \
    cd repo && \
    jj git init && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    echo "Initial content" > file.txt && \
    jj new -m "Initial commit"

# Container contents:
#   - /home/user/repo - jj repository with an initial commit
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
