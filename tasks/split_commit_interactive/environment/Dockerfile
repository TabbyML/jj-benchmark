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
LABEL Description="jj project with a single commit containing two features to be split."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj git init . && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    echo "print('A')" > feature_a.py && \
    echo "print('B')" > feature_b.py && \
    jj commit -m "Add feature A and feature B"

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/myproject  — jj repository with a commit containing feature_a.py and feature_b.py

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]