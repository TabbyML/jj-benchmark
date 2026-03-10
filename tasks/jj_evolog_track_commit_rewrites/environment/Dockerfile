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
LABEL Description="jj repo in /home/user/project with a commit rewritten 3 times via amend/squash, for evolog tracking exercise."

RUN jj git init /home/user/project && \
    cd /home/user/project && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/project && \
    printf '# auth module v1\ndef authenticate(user):\n    return True\n' > /home/user/project/auth.py && \
    jj describe -m "feat: add authentication module" && \
    jj new && \
    printf 'def get_token(user):\n    return "token_v1"\n' >> /home/user/project/auth.py && \
    jj squash -m "feat: add authentication module" && \
    jj new && \
    printf '# auth utilities\ndef validate_token(token):\n    return token is not None\n' > /home/user/project/auth_utils.py && \
    jj describe -m "fix: auth token handling" && \
    jj squash -m "feat: add authentication module"

# Container contents:
#   - /home/user/project  — jj repository with one commit above root:
#       - "feat: add authentication module" (auth.py + auth_utils.py)
#       - evolog for @ shows 3 entries: current + 2 predecessors

CMD ["/bin/bash"]
