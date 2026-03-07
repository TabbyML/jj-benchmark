FROM ubuntu:22.04

LABEL Author="jj-task-builder"

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
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV EDITOR=true
ENV JJ_CONFIG=/home/user/.config/jj/config.toml

RUN mkdir -p /home/user/.config/jj && \
    printf '[user]\nname = "Dev User"\nemail = "dev@example.com"\n' \
    > /home/user/.config/jj/config.toml

RUN mkdir -p /home/user/upstream-project/src

WORKDIR /home/user/upstream-project

RUN jj git init --colocate .

# Commit 1: main-v1
RUN printf 'def load_data(path):\n    return open(path).read()\n' > src/data.py && \
    jj describe -m "chore: initial scaffold" && \
    jj bookmark create main -r @

# Commit 2: main-v2 (upstream context-manager fix)
RUN jj new -m "fix: use context manager in load_data" && \
    printf 'def load_data(path):\n    with open(path) as f:\n        return f.read()\n' > src/data.py && \
    jj bookmark create main-v2 -r @

# Go back to main-v1 to build feature stack
RUN jj new main -m "feat: implement process_data function"

# Commit 3: feature-patch-1 (adds process_data on top of main-v1)
RUN printf 'def load_data(path):\n    return open(path).read()\n\ndef process_data(raw):\n    return raw.strip()\n' > src/data.py

# Commit 4: feature-patch-2 (adds logging)
RUN jj new -m "feat: add logging to process_data" && \
    printf 'def load_data(path):\n    return open(path).read()\n\ndef process_data(raw):\n    import sys\n    result = raw.strip()\n    print("processed", file=sys.stderr)\n    return result\n' > src/data.py && \
    jj bookmark create feature -r @

# Create empty working-copy on top of feature
RUN jj new -m ""

CMD ["/bin/bash"]
