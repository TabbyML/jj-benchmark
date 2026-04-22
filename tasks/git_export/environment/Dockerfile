FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="A non-colocated Jujutsu repo backed by a Git repo with unexported bookmarks."

RUN mkdir -p /home/user/git-repo && \
    cd /home/user/git-repo && \
    git init && \
    git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    echo "init" > file.txt && \
    git add file.txt && \
    git commit -m "init"

RUN mkdir -p /home/user/jj-repo && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init --no-colocate --git-repo /home/user/git-repo /home/user/jj-repo && \
    cd /home/user/jj-repo && \
    echo "jj" > file.txt && \
    jj bookmark create feature-x && \
    jj commit -m "jj commit"

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/git-repo - the backing Git repository
#   - /home/user/jj-repo - the non-colocated Jujutsu repository
#   - feature-x bookmark created in jj-repo but not exported to git-repo

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
