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
LABEL Description="jj obslog view task environment."

RUN mkdir -p /root/.config/jj && \
    echo '[user]' > /root/.config/jj/config.toml && \
    echo 'name = "Test User"' >> /root/.config/jj/config.toml && \
    echo 'email = "test@example.com"' >> /root/.config/jj/config.toml && \
    mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init . && \
    echo "v1" > file.txt && \
    jj describe -m "v1" && \
    echo "v2" > file.txt && \
    jj describe -m "v2"

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/repo — a jj repository with an evolved working copy commit

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]