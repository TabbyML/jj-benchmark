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
RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

LABEL Author="any-task-builder"
LABEL Description="A colocated Jujutsu repository with a new Git commit that needs to be imported."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    git init && \
    echo "initial" > file.txt && \
    git add file.txt && \
    git commit -m "initial commit" && \
    jj git init --colocate && \
    echo "new" > file.txt && \
    git commit -am "new commit"

# Container contents:
#   - jj installed via binary release.
#   - /home/user/project - a colocated git/jj repository with an initial commit, initialized jj, and a new git commit.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
