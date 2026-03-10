FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj Git colocated interoperability task environment — existing Git repo for jj colocation workflow"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure git global identity (needed for git commit in bootstrap)
RUN git config --global user.email "bootstrap@example.com" && \
    git config --global user.name "Bootstrap" && \
    git config --global init.defaultBranch main

# Bootstrap: create a plain Git repo with two commits
RUN mkdir -p /home/user/gitrepo && \
    cd /home/user/gitrepo && \
    git init && \
    git config user.email "bootstrap@example.com" && \
    git config user.name "Bootstrap" && \
    echo "# My Project" > README.md && \
    git add README.md && \
    git commit -m "initial commit" && \
    git branch -M main 2>/dev/null || true && \
    echo '[settings]' > config.toml && \
    git add config.toml && \
    git commit -m "add config"

CMD ["/bin/bash"]
