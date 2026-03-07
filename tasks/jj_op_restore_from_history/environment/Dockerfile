FROM ubuntu:22.04

# Install system dependencies: curl, ca-certificates, git, python3, python3-pip, bash
# Then install pytest via pip3
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip bash && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install jj from the official release
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo at /home/user/project with two commits (add base module, refactor: squash target) where the squash target has been squashed into its parent. The user must use jj op log and jj op restore to recover the standalone refactor: squash target commit."

# Set up the repository environment matching jujutsu_setup bootstrap script.
# EDITOR=true prevents any editor from opening during non-interactive commands.
ENV EDITOR=true

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf '# base module\ndef base():\n    return "base"\n' > base.py && \
    jj describe -m "add base module" && \
    jj new && \
    printf '# refactor module\ndef refactor():\n    return "refactored"\n' > refactor.py && \
    jj describe -m "refactor: squash target" && \
    jj new && \
    jj prev --edit && \
    jj squash --use-destination-message

# Container contents:
#   - /home/user/project  — jj repository with:
#       1. "add base module" commit (contains base.py and refactor.py after squash)
#       2. Empty working copy (@) on top
#   - The "refactor: squash target" commit has been squashed away (op log has the squash operation)
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
