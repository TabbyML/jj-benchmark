FROM ubuntu:24.04

RUN apt-get update && apt-get install -y curl python3 python3-pip git && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin ./jj && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="conflict_resolution task for jj"

RUN cd /home/user && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj git init && \
    echo "Line 1\nLine 2\nLine 3" > file.txt && \
    jj bookmark create main && \
    jj describe -m "Initial commit" && \
    jj new main -m "Feature A" && \
    echo "Line 1\nFeature A\nLine 3" > file.txt && \
    jj bookmark create feature-a && \
    jj new main -m "Feature B" && \
    echo "Line 1\nFeature B\nLine 3" > file.txt && \
    jj bookmark create feature-b

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
