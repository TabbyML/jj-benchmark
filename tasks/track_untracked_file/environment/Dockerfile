FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="jj project with an ignored file app.log in /home/user/project."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init && \
    echo "*.log" > .gitignore && \
    echo "test log" > app.log && \
    jj commit -m "Initial commit"

# Container contents:
#   - jj installed for the task.
#   - /home/user/project  - jj repository with .gitignore and app.log
#   - .gitignore with *.log
#   - app.log which is ignored and untracked

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
