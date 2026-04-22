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
LABEL Description="Jujutsu task environment with an initialized repository and specific commit history."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init --colocate && \
    echo 'DEBUG = False' > config.py && \
    echo 'def helper(): return "v1"' > utils.py && \
    echo 'print("v1 app")' > app.py && \
    jj commit -m "Initial commit" && \
    jj bookmark create v1.0 -r @- && \
    echo 'DEBUG = False\nPORT = 8080' > config.py && \
    echo 'def helper(): return "v2"' > utils.py && \
    echo 'print("v2 app")' > app.py && \
    jj commit -m "Update files" && \
    echo 'DEBUG = True\nPORT = 8080' > config.py && \
    echo 'def helper(): return "working copy utils"' > utils.py && \
    echo 'print("working copy app")' > app.py

# Container contents:
#   - jj installed in /usr/local/bin
#   - /home/user/myproject initialized as a jj repository
#   - v1.0 bookmark and multiple commits set up for the revert task

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
