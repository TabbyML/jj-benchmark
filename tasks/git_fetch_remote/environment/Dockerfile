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
LABEL Description="jj git fetch and rebase task environment"

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    mkdir -p /home/user/remote.git && \
    cd /home/user/remote.git && \
    git init --bare && \
    cd /home/user && \
    git clone /home/user/remote.git remote_work && \
    cd remote_work && \
    git checkout -b main && \
    echo "Initial commit" > file.txt && \
    git add file.txt && \
    git commit -m "Initial commit" && \
    git push origin main && \
    cd /home/user && \
    jj git clone /home/user/remote.git repo && \
    cd repo && \
    jj bookmark create feature && \
    echo "Feature commit" > feature.txt && \
    jj commit -m "Feature commit" && \
    cd /home/user/remote_work && \
    echo "Update main" > file.txt && \
    git add file.txt && \
    git commit -m "Update main" && \
    git push origin main && \
    rm -rf /home/user/remote_work

# Container contents:
#   - jj installed
#   - /home/user/repo: jj repository with feature bookmark
#   - /home/user/remote.git: bare Git repository with an updated main branch

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
