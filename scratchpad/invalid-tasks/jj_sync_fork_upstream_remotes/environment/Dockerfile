FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: sync a fork with multiple remotes (upstream + origin) as an open-source maintainer"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# ── Create upstream bare repo with 3 commits ─────────────────────────────────
RUN git init --bare /home/user/remotes/upstream.git

RUN git clone /home/user/remotes/upstream.git /tmp/tmp_upstream \
    && git -C /tmp/tmp_upstream config user.email "upstream@example.com" \
    && git -C /tmp/tmp_upstream config user.name "Upstream Author" \
    && echo "# MyProject" > /tmp/tmp_upstream/README.md \
    && git -C /tmp/tmp_upstream add README.md \
    && git -C /tmp/tmp_upstream commit -m "Initial commit" \
    && echo "def core(): pass" > /tmp/tmp_upstream/core.py \
    && git -C /tmp/tmp_upstream add core.py \
    && git -C /tmp/tmp_upstream commit -m "Add core library" \
    && echo "def upstream_feature(): pass" > /tmp/tmp_upstream/upstream_feature.py \
    && git -C /tmp/tmp_upstream add upstream_feature.py \
    && git -C /tmp/tmp_upstream commit -m "Add upstream feature" \
    && git -C /tmp/tmp_upstream push origin main \
    && rm -rf /tmp/tmp_upstream

# ── Create origin bare repo with only 2 commits ──────────────────────────────
RUN git init --bare /home/user/remotes/origin.git

RUN git clone /home/user/remotes/upstream.git /tmp/tmp_origin \
    && git -C /tmp/tmp_origin config user.email "fork@example.com" \
    && git -C /tmp/tmp_origin config user.name "Fork Author" \
    && SECOND_COMMIT=$(git -C /tmp/tmp_origin rev-parse HEAD~1) \
    && git -C /tmp/tmp_origin push "file:///home/user/remotes/origin.git" "${SECOND_COMMIT}:refs/heads/main" \
    && rm -rf /tmp/tmp_origin

# ── Create the working jj repo ───────────────────────────────────────────────
RUN mkdir -p /home/user/myproject \
    && jj git init --colocate /home/user/myproject

RUN cd /home/user/myproject \
    && jj config set --repo user.email "maintainer@example.com" \
    && jj config set --repo user.name "Maintainer" \
    && jj git remote add origin "file:///home/user/remotes/origin.git" \
    && jj git remote add upstream "file:///home/user/remotes/upstream.git" \
    && jj git fetch --remote origin \
    && jj bookmark set main -r "main@origin" \
    && jj new main -m "Add WIP feature work" \
    && echo "def wip_feature(): pass" > wip.py \
    && jj bookmark set wip-feature -r @ \
    && jj new wip-feature

WORKDIR /home/user/myproject

CMD ["/bin/bash"]
