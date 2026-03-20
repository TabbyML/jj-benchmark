FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj config set --user user.name "Maintainer" && \
    jj config set --user user.email "maintainer@example.com"

RUN git config --global user.name "Maintainer" && \
    git config --global user.email "maintainer@example.com"

RUN jj git init /home/user/repo

RUN cd /home/user/repo && \
    jj config set --repo user.name "Maintainer" && \
    jj config set --repo user.email "maintainer@example.com"

# Build shared history (before divergence)
RUN cd /home/user/repo && \
    printf '# Shared Project\n' > README.md && \
    jj describe -m "init: shared base" && \
    jj new

RUN cd /home/user/repo && \
    mkdir -p src && \
    printf 'VERSION = "1.0"\n' > src/version.py && \
    jj describe -m "feat: shared-v1" && \
    jj new

RUN cd /home/user/repo && \
    printf 'CONFIG = "base"\n' > src/config.py && \
    jj describe -m "feat: shared-config" && \
    jj new

RUN cd /home/user/repo && \
    printf 'def utils(): pass\n' > src/utils.py && \
    jj describe -m "feat: shared-utils"

# Create divergence point - set both bookmarks here
RUN cd /home/user/repo && \
    jj bookmark create main -r @ && \
    jj bookmark create develop -r @

# main branch: 5 more commits
RUN cd /home/user/repo && \
    jj new main && \
    printf 'RELEASE = "1.1"\n' > src/release.py && \
    jj describe -m "release: v1.1" && \
    jj bookmark move main --to @

RUN cd /home/user/repo && \
    jj new main && \
    printf 'PATCH = "1"\n' > src/patch.py && \
    jj describe -m "fix: patch-1" && \
    jj bookmark move main --to @

RUN cd /home/user/repo && \
    jj new main && \
    printf 'SECURITY = "1"\n' > src/security.py && \
    jj describe -m "fix: security-update" && \
    jj bookmark move main --to @

RUN cd /home/user/repo && \
    jj new main && \
    printf 'RELEASE = "1.2"\n' > src/release12.py && \
    jj describe -m "release: v1.2" && \
    jj bookmark move main --to @

RUN cd /home/user/repo && \
    jj new main && \
    printf 'HOTFIX = "1"\n' > src/hotfix.py && \
    jj describe -m "fix: hotfix-critical" && \
    jj bookmark move main --to @

# develop branch: 5 different commits
RUN cd /home/user/repo && \
    jj new develop && \
    printf 'FEATURE_X = True\n' > src/feature_x.py && \
    jj describe -m "feat: feature-x-start" && \
    jj bookmark move develop --to @

RUN cd /home/user/repo && \
    jj new develop && \
    printf 'FEATURE_X_V2 = True\n' > src/feature_x_v2.py && \
    jj describe -m "feat: feature-x-complete" && \
    jj bookmark move develop --to @

RUN cd /home/user/repo && \
    jj new develop && \
    printf 'EXPERIMENT = True\n' > src/experiment.py && \
    jj describe -m "feat: experimental-api" && \
    jj bookmark move develop --to @

RUN cd /home/user/repo && \
    jj new develop && \
    printf 'REFACTOR = True\n' > src/refactored.py && \
    jj describe -m "refactor: code-cleanup" && \
    jj bookmark move develop --to @

RUN cd /home/user/repo && \
    jj new develop && \
    printf 'NEW_FEATURE = True\n' > src/new_feature.py && \
    jj describe -m "feat: new-feature-prep" && \
    jj bookmark move develop --to @

LABEL Author="jj-task-builder"
LABEL Description="Repo with diverged main and develop branches - agent must find LCA and document divergence"

CMD ["/bin/bash"]
