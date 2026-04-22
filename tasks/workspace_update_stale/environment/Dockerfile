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
LABEL Description="A jj repository with a stale workspace."

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj git init . && \
    echo '{"status": "pending"}' > config.json && \
    jj commit -m "initial" && \
    jj workspace add ../workspace_b && \
    cd ../workspace_b && \
    echo '{"status": "pending", "new": true}' > config.json && \
    jj commit -m "update config" && \
    jj rebase -r default@ -d @

# Container contents:
#   - jj v0.38.0 installed.
#   - /home/user/myproject  - jj repository (stale workspace)
#   - /home/user/workspace_b - another workspace that modified the repo
#   - config.json in workspace_b with {"status": "pending", "new": true}

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
