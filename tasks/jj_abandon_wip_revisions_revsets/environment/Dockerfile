FROM ubuntu:22.04

LABEL Author="jj-task-builder"

ENV DEBIAN_FRONTEND=noninteractive
ENV EDITOR=true

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Install jj from official release
RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure jj user identity
RUN jj config set --user user.name "Dev User" \
    && jj config set --user user.email "dev@example.com"

# Set up the mylib repository
RUN mkdir -p /home/user/mylib/src

WORKDIR /home/user/mylib

RUN jj git init

# Commit 1: Initial project scaffold (README.md), bookmark: main
RUN echo "# mylib" > /home/user/mylib/README.md \
    && jj describe -m "Initial project scaffold" \
    && jj bookmark create main -r @

# Commit 2: Add core library module (src/lib.rs), bookmark: feature/core
RUN jj new \
    && echo "// core library" > /home/user/mylib/src/lib.rs \
    && jj describe -m "Add core library module" \
    && jj bookmark create feature/core -r @

# WIP scratch commit A: child of feature/core, empty description
RUN jj new feature/core \
    && echo "scratch work A" > /home/user/mylib/wip_a.txt

# WIP scratch commit B: another child of feature/core, empty description
RUN jj new feature/core \
    && echo "scratch work B" > /home/user/mylib/wip_b.txt

# Set working copy to feature/core so README.md and src/lib.rs are visible
RUN jj edit feature/core

CMD ["/bin/bash"]
