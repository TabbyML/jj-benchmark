FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="jj workspace environment with a deeply nested directory."

RUN git config --global user.name "Your Name" && \
    git config --global user.email "your@email.com" && \
    jj config set --user user.name "Your Name" && \
    jj config set --user user.email "your@email.com"

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init --colocate && \
    mkdir -p /home/user/repo/deeply/nested/dir

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/repo - jj initialized repository
#   - /home/user/repo/deeply/nested/dir - nested directory within the workspace

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
