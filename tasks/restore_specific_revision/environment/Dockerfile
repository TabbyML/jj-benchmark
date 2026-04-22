FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Jujutsu repository with a file modified across multiple commits."

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init --colocate && \
    echo "version=1" > config.txt && \
    jj commit -m "v1" && \
    echo "version=2" > config.txt && \
    jj commit -m "v2" && \
    echo "version=3" > config.txt

# Container contents:
#   - jj installed in /usr/local/bin
#   - /home/user/repo - jj repository with config.txt modified in working copy
#   - config.txt currently contains version=3, parent commit has version=2

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
