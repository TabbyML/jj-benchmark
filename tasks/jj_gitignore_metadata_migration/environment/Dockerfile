FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.34.0/jj-v0.34.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with tracked files that need to be untracked and ignored."

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test.user@example.com" && \
    mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init . && \
    echo 'print("Hello World")' > main.py && \
    echo "initial log entry" > app.log && \
    echo '{"env": "local"}' > config.local.json && \
    jj describe -m "Initial commit with config and logs" && \
    jj new

# Container contents:
#   - /home/user/project  — jj repository with tracked files (app.log, config.local.json, main.py)
#       - "Initial commit with config and logs"
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
