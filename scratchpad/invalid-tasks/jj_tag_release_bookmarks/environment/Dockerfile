FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: tag release bookmarks - create auth-v1.0, payments-v1.0, and move main bookmark"

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

RUN mkdir -p /home/user/release-project

RUN jj git init /home/user/release-project

RUN jj --repository /home/user/release-project config set --repo user.name "Release Manager"
RUN jj --repository /home/user/release-project config set --repo user.email "release@example.com"

RUN jj --repository /home/user/release-project describe -m "initial project scaffold"
RUN jj --repository /home/user/release-project new

RUN jj --repository /home/user/release-project describe -m "add authentication module"
RUN jj --repository /home/user/release-project new

RUN jj --repository /home/user/release-project describe -m "add payment gateway"
RUN jj --repository /home/user/release-project new

RUN jj --repository /home/user/release-project describe -m "add reporting dashboard"

RUN AUTH_CHANGE_ID=$(jj --repository /home/user/release-project log --no-graph \
        -r 'description(substring:"add authentication module")' \
        --template 'change_id.short()' --color never | head -1 | tr -d '[:space:]') && \
    jj --repository /home/user/release-project bookmark create main -r "$AUTH_CHANGE_ID"

CMD ["/bin/bash"]
