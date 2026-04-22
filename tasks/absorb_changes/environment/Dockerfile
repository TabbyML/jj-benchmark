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
LABEL Description="jj project with a stack of commits and uncommitted bug fixes in the working copy."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf "def feature_a():\n    print('A')\n" > feature_a.py && \
    printf "def feature_b():\n    print('B')\n" > feature_b.py && \
    jj new -m "Initial commit" && \
    printf "def feature_a():\n    print('Feature A')\n" > feature_a.py && \
    jj new -m "Add feature A" && \
    printf "def feature_b():\n    print('Feature B')\n" > feature_b.py && \
    jj new -m "Add feature B" && \
    printf "def feature_a():\n    print('Feature A fixed')\n" > feature_a.py && \
    printf "def feature_b():\n    print('Feature B fixed')\n" > feature_b.py

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/project initialized as a jj repository
#   - Stack of commits with features A and B
#   - Working copy containing bug fixes to both features

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
