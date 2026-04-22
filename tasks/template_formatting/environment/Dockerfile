FROM ubuntu:24.04

# Pre-requisites
RUN apt-get update && apt-get install -y --no-install-recommends curl python3 python3-pip && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    pip3 install --break-system-packages uv && \
    rm -rf /var/lib/apt/lists/*

# Install target library
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user/myproject && chmod 0755 /home/user && chmod 0755 /home/user/myproject

LABEL Author="any-task-builder"
LABEL Description="Empty environment with jj installed and an empty project directory."

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/myproject directory ready for use

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
