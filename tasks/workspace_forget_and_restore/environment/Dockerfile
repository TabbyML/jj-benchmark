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
LABEL Description="jj repository with one commit and default workspace."

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init . && \
    echo "initial content" > initial.txt && \
    jj new -m "Initial commit" && \
    jj commit -m "Add initial file"

# Container contents:
#   - /home/user/repo - jj repository with one commit
#   - jj configured with a test user

CMD ["/bin/bash"]