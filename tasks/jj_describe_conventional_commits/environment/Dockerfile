FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL task="jj_describe_conventional_commits"
LABEL description="Release manager describe commits with Conventional Commits format"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV HOME=/home/user
ENV EDITOR=true
ENV JJ_NO_PAGER=1
ENV PAGER=cat

RUN jj git init /home/user/project

WORKDIR /home/user/project

RUN jj config set --repo user.name "Dev User" && \
    jj config set --repo user.email "dev@example.com"

RUN echo "# My Project" > README.md && \
    jj describe -m "chore: initialize project" && \
    jj new

RUN mkdir -p src && \
    echo "# REST API module" > src/api.py && \
    jj new

RUN echo "# CLI module" > src/cli.py && \
    jj new

RUN jj log --no-graph -r 'all()' -T 'change_id.short() ++ " | " ++ description ++ "\n"'

CMD ["/bin/bash"]
