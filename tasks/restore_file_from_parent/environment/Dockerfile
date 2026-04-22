FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Jujutsu repository with modified files in the working copy to test file restoration."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj git init --colocate && \
    jj config set --user user.name "Your Name" && \
    jj config set --user user.email "your@email.com" && \
    echo 'print("Hello World - v1")' > app.py && \
    echo 'port=8080' > config.txt && \
    jj new && \
    echo 'print("Hello World - v2")' > app.py && \
    echo 'port=9090' > config.txt

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/myproject - Jujutsu repository
#   - config.txt modified to port=9090 (parent has port=8080)
#   - app.py modified to Hello World - v2 (parent has Hello World - v1)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
