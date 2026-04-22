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
LABEL Description="Jujutsu repository with a bookmark to be renamed."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj git init --colocate && \
    jj config set --repo user.name "Your Name" && \
    jj config set --repo user.email "your@email.com" && \
    echo "test" > test.txt && \
    jj bookmark create old-feature

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/myproject - A jj repository
#   - A bookmark named 'old-feature'

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]