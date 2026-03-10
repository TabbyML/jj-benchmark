FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL description="jj task: recover an accidentally abandoned commit using the operation log and jj undo"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Initialize the support-repo
RUN mkdir -p /home/user/support-repo \
    && cd /home/user/support-repo \
    && jj git init . \
    && jj config set --repo user.name "Support Engineer" \
    && jj config set --repo user.email "support@example.com"

# Create initial commit with README.md
RUN cd /home/user/support-repo \
    && echo "# Support Repo" > README.md \
    && jj describe -m "initial: add README" \
    && jj new

# Create the important bug-fix commit
RUN cd /home/user/support-repo \
    && mkdir -p src \
    && printf 'def handle_request(req):\n    if req is None: return\n    return req.process()\n' > src/handler.py \
    && jj describe -m "fix: patch null pointer dereference in request handler" \
    && jj new

# Accidentally abandon the bug-fix commit
RUN cd /home/user/support-repo \
    && jj abandon @-

CMD ["/bin/bash"]
