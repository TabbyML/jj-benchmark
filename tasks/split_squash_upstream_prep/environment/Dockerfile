FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: split and squash commits to prepare a clean upstream submission"

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install pytest

# Install jj from official release
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

# Create /home/user
RUN mkdir -p /home/user && chmod 0755 /home/user

# Bootstrap the repository
RUN mkdir -p /home/user/mylib \
    && cd /home/user/mylib \
    && jj git init \
    && jj config set --repo user.name "Test User" \
    && jj config set --repo user.email "test@example.com" \
    && mkdir -p src tests \
    && echo "# mylib" > README.md \
    && jj describe -m "initial commit" \
    && jj new \
    && printf 'def greet(name):\n    return f"Hello, {name}!"\n' > src/utils.py \
    && printf 'def parse_config(path):\n    return {"path": path}\n' > src/config.py \
    && printf 'def test_parse_config():\n    assert parse_config("a") == {"path": "a"}\n' > tests/test_config.py \
    && jj describe -m "add config parser and update tests" \
    && jj new

CMD ["/bin/bash"]
