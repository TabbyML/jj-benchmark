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

LABEL Author="jj-task-builder"
LABEL Description="jj repo setup for bookmark management task"

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init . && \
    jj config set --repo user.name 'Test User' && \
    jj config set --repo user.email 'test@example.com' && \
    echo 'initial content' > main.py && \
    jj describe -m 'initial commit' && \
    jj bookmark create main && \
    jj new && \
    echo 'auth logic v1' > auth.py && \
    jj describe -m 'feat: basic auth' && \
    jj bookmark create auth-feature && \
    jj new && \
    echo 'auth logic v2' > auth.py

# Container contents:
# • /home/user/repo — jj repository with:
#   - Root commit
#   - "initial commit" (bookmark: main)
#   - "feat: basic auth" (bookmark: auth-feature)
#   - Working copy with modified auth.py (auth logic v2)
# • Python 3, pip, and pytest available.

CMD ["/bin/bash"]