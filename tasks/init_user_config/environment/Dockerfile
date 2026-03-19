FROM ubuntu:22.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip bash && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN mkdir -p /home/user/myproject && \
    echo "# My Project" > /home/user/myproject/README.md

LABEL Author="jj-task-builder"
LABEL Description="Developer migrating from Git: /home/user/myproject exists with README.md; user must init jj repo and set user identity."

CMD ["/bin/bash"]
