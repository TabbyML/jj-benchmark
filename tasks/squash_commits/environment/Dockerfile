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
LABEL Description="jj project with a chain of commits in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    git init && \
    jj git init --colocate && \
    jj config set --repo user.name "Your Name" && \
    jj config set --repo user.email "your@email.com" && \
    echo "def init(): pass" > app.py && \
    jj commit -m "init" && \
    echo -e "def init(): pass\n\ndef feature_a(): pass" > app.py && \
    jj commit -m "add feature A" && \
    echo -e "def init(): pass\n\ndef feature_a(): pass\n\ndef feature_b(): pass" > app.py && \
    jj commit -m "add feature B" && \
    echo -e "def init(): pass\n\ndef feature_a(): pass\n\ndef feature_b(): pass\n\ndef feature_c(): pass" > app.py && \
    jj commit -m "add feature C"

# Container contents:
#   - jj installed for jj project.
#   - /home/user/myproject  — jj project with initial commits
#   - app.py with multiple features

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
