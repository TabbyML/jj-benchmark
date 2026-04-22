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
LABEL Description="jj project with a main and feature branch to test rebasing to a destination."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj config set --user user.name "User" && \
    jj config set --user user.email "user@example.com" && \
    jj git init --colocate && \
    echo "A" > file.txt && \
    jj bookmark create main && \
    jj new main -m "Feature commit" && \
    echo "B" > feature.txt && \
    jj bookmark create feature && \
    jj new main -m "Main commit" && \
    echo "C" > main.txt && \
    jj bookmark move main --to @

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/myproject  — jj project with main and feature branches

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
