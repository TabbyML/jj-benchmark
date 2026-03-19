FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.34.0/jj-v0.34.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with divergent commits on a single bookmark in /home/user/repo."

RUN git init /home/user/remote_repo && \
    jj git init --colocate /home/user/remote_repo && \
    cd /home/user/remote_repo && \
    jj config set --repo user.name "Remote User" && \
    jj config set --repo user.email "remote@example.com" && \
    echo "def main(): pass" > main.py && \
    jj describe -m "feature base" && \
    jj bookmark create feature -r @ && \
    jj new && \
    cd /home/user && \
    jj git clone /home/user/remote_repo repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    jj config set --repo 'revset-aliases."immutable_heads()"' '"none()"' && \
    jj edit feature && \
    echo "def main(): print('local feature')" > main.py && \
    jj describe -m "feature base with local feature" && \
    jj new && \
    cd /home/user/remote_repo && \
    jj config set --repo 'revset-aliases."immutable_heads()"' '"none()"' && \
    jj edit feature && \
    echo "def main(): print('remote bugfix')" > main.py && \
    jj describe -m "feature base with remote bugfix" && \
    jj new && \
    cd /home/user/repo && \
    jj git fetch || true

# Container contents:
#   - /home/user/remote_repo - the remote git/jj repository
#   - /home/user/repo  - local jj repository with a divergent 'feature' bookmark
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
