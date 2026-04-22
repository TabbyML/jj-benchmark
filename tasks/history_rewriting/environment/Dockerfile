FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y curl tar git && \
    curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="A jj repository with a stack of commits."

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init && \
    echo "old" > base.txt && \
    jj new -m "Base" && \
    echo "c1" > c1.txt && \
    jj new -m "Commit 1" && \
    echo "c2" > c2.txt && \
    jj new -m "Commit 2" && \
    echo "c3" > c3.txt && \
    jj new -m "Commit 3"

# Container contents:
#   - jj installed
#   - /home/user/repo initialized with a stack of 4 commits

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
