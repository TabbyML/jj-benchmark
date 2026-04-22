FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl tar git && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN useradd -m -s /bin/bash user
USER user
WORKDIR /home/user

RUN mkdir -p /home/user/repo
WORKDIR /home/user/repo

RUN jj git init --colocate && \
    jj config set --user user.name "Initial Author" && \
    jj config set --user user.email "initial@example.com" && \
    echo "initial" > initial.txt && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new

CMD ["bash"]
