FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y nodejs && \
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Jujutsu project environment with an initialized repo for bookmark management."

RUN mkdir -p /home/user/my-project && \
    cd /home/user/my-project && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init

# Container contents:
#   - jj installed in /usr/local/bin.
#   - /home/user/my-project  — initialized jj repository.
#   - Default jj config set up.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
