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
LABEL Description="jj concurrent operations task environment with a pre-configured repo."

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    jj new -m 'Feature X' && \
    jj describe -m 'Feature X - variant 1'

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/repo  - initialized jj repository with a commit and its variant

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
