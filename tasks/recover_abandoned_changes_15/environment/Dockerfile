FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with an abandoned bug fix commit in /home/user/workspace/repo."

RUN mkdir -p /home/user/workspace && \
    jj git init /home/user/workspace/repo && \
    cd /home/user/workspace/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    mkdir -p src && \
    touch src/bugfix.py && \
    jj describe -m "Initial commit" && \
    jj new && \
    echo "def fix_bug(): return True" > src/bugfix.py && \
    jj describe -m "Fix the bug" && \
    jj abandon

# Container contents:
#   - /home/user/workspace/repo  — jj repository with an initial commit and an abandoned bug fix commit:
#       - "Initial commit" (empty src/bugfix.py)
#       - "Fix the bug" (abandoned, contains bug fix in src/bugfix.py)
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
