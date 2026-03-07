FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: resolve conflict in stacked commits by manually editing conflict markers"

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

# Install jj v0.38.0
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Bootstrap: set up the repository environment
WORKDIR /home/user

RUN mkdir -p /home/user/project
WORKDIR /home/user/project

RUN jj git init

RUN jj config set --repo user.name "Test User"
RUN jj config set --repo user.email "test@example.com"

# Commit 1: init-config (main)
RUN mkdir -p config && \
    printf '[server]\nhost = "localhost"\nport = 8080\n\n[database]\nurl = "postgres://localhost/mydb"\npool_size = 5\n' > config/settings.toml && \
    jj describe -m "init-config" && \
    jj bookmark create main -r @

# Commit 2: update-server-config (feature-server)
RUN jj new -m "update-server-config" && \
    printf '[server]\nhost = "0.0.0.0"\nport = 9090\n\n[database]\nurl = "postgres://localhost/mydb"\npool_size = 5\n' > config/settings.toml && \
    jj bookmark create feature-server -r @

# Commit 3: update-db-config — created from main, then rebased onto feature-server
RUN jj new -r main -m "update-db-config" && \
    printf '[server]\nhost = "localhost"\nport = 8081\n\n[database]\nurl = "postgres://localhost/mydb"\npool_size = 10\n' > config/settings.toml && \
    jj rebase -r @ -d feature-server && \
    jj bookmark create feature-db -r @

CMD ["/bin/bash"]
