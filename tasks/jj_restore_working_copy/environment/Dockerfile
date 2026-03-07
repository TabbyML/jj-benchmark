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
LABEL Description="jj repo at /home/user/project with 3 commits (chore: add config, feat: add parser, wip: partial refactor); parser.py contains the wrong upper() implementation to be restored."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf '[settings]\nversion = 1\n' > config.toml && \
    jj describe -m "chore: add config" && \
    jj new && \
    printf '# parser module\ndef parse(text):\n    return text.strip()\n' > parser.py && \
    jj describe -m "feat: add parser" && \
    jj new && \
    printf '# parser module\ndef parse(text):\n    return text.upper()\n' > parser.py && \
    jj describe -m "wip: partial refactor"

# Container contents:
#   - /home/user/project  — jj repository with three commits above root:
#       1. "chore: add config"  (config.toml with [settings] version = 1)
#       2. "feat: add parser"   (parser.py with return text.strip())
#       3. "wip: partial refactor" — working copy @ (parser.py with return text.upper())
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
