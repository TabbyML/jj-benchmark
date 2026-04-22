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
LABEL Description="Jujutsu repository with a tracked build.log file that should be ignored."

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init && \
    echo "This is a build log" > build.log && \
    jj commit -m "initial commit"

# Container contents:
#   - jj installed in /usr/local/bin
#   - /home/user/project  — jj repository
#   - build.log is tracked by jj

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
