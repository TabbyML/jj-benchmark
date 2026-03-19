FROM ubuntu:24.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip python3-pytest bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj config set --user user.name "Test User" && jj config set --user user.email "test@example.com"

WORKDIR /home/user

# Initialize git-backed jj repo
RUN jj git init repo

WORKDIR /home/user/repo

# Create src directory structure
RUN mkdir -p src

# Create initial files on main branch
RUN echo "# core module v1" > src/core.py && \
    echo "def init(): pass" >> src/core.py && \
    jj describe -m "chore: initial project setup"

RUN jj new && \
    echo "# utils module" > src/utils.py && \
    jj describe -m "chore: add utils module"

RUN jj new && \
    echo "# config module" > src/config.py && \
    jj describe -m "chore: add config module"

# Create main bookmark at current commit
RUN jj bookmark create main -r @

# Create feature-a branch from main
RUN jj new main && \
    echo "def feature_a_func(): return 'a'" >> src/core.py && \
    jj describe -m "feat: feature-a adds core function"

RUN jj new && \
    echo "# feature-a module" > src/feature_a.py && \
    jj describe -m "feat: feature-a adds dedicated module"

RUN jj new && \
    echo "def feature_a_helper(): pass" >> src/core.py && \
    jj describe -m "feat: feature-a extends core with helper" && \
    jj bookmark create feature-a -r @

# Create feature-b branch from main
RUN jj new main && \
    echo "# feature-b module" > src/feature_b.py && \
    jj describe -m "feat: feature-b adds dedicated module"

RUN jj new && \
    echo "def feature_b_func(): return 'b'" >> src/core.py && \
    jj describe -m "feat: feature-b modifies core" && \
    jj bookmark create feature-b -r @

# Create feature-c branch from feature-a (overlapping ancestry)
RUN jj new feature-a && \
    echo "# feature-c module" > src/feature_c.py && \
    jj describe -m "feat: feature-c adds dedicated module"

RUN jj new && \
    echo "def feature_c_func(): return 'c'" >> src/core.py && \
    jj describe -m "feat: feature-c modifies core too" && \
    jj bookmark create feature-c -r @

# Go back to a clean working state
RUN jj new main

CMD ["/bin/bash"]
