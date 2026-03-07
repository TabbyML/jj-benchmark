FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && pip3 install pytest \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV JJ_USER="Test User"
ENV JJ_EMAIL="test@example.com"

RUN git init --bare /home/user/remotes/origin.git \
    && git init --bare /home/user/remotes/upstream.git

RUN mkdir -p /home/user/myproject \
    && cd /home/user/myproject \
    && jj git init --no-colocate . \
    && jj config set --repo user.name "Test User" \
    && jj config set --repo user.email "test@example.com"

RUN cd /home/user/myproject \
    && echo "# My Project" > README.md \
    && jj describe -m "initial commit" \
    && jj bookmark create main -r @ \
    && jj git remote add origin /home/user/remotes/origin.git \
    && jj git remote add upstream /home/user/remotes/upstream.git

RUN cd /home/user/myproject \
    && jj git export \
    && GIT_DIR="$(jj git root)" \
    && MAIN_SHA="$(git --git-dir="$GIT_DIR" rev-parse main)" \
    && git --git-dir="$GIT_DIR" push /home/user/remotes/origin.git "${MAIN_SHA}:refs/heads/main" \
    && git --git-dir="$GIT_DIR" push /home/user/remotes/upstream.git "${MAIN_SHA}:refs/heads/main" \
    && jj git fetch --remote origin \
    && jj git fetch --remote upstream \
    && jj bookmark track main --remote=origin \
    && jj bookmark track main --remote=upstream

RUN cd /home/user/myproject \
    && jj new main -m "add feature" \
    && echo "feature content" > feature.txt \
    && jj bookmark create feature -r @ \
    && jj new

CMD ["/bin/bash"]
