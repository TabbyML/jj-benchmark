FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL task="jj_create_move_bookmarks"
LABEL description="Release manager create and move bookmarks task for jj"

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
    echo "# User login module" > src/login.py && \
    jj describe -m "feat: implement user login" && \
    jj new

RUN echo "# Password reset module" > src/reset.py && \
    jj describe -m "feat: implement password reset" && \
    jj new

RUN jj bookmark create feature/auth -r @--

RUN jj log --no-graph -r 'all()' -T 'description ++ "\n"' && \
    jj bookmark list

CMD ["/bin/bash"]
