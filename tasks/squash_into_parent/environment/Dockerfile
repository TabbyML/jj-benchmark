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
LABEL Description="jj repo at /home/user/monorepo with 3 commits; working copy 'wip: fixup lint flag' to be squashed into parent."

RUN mkdir -p /home/user/monorepo && \
    cd /home/user/monorepo && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf 'all:\n\techo done\n' > Makefile && \
    jj describe -m "build: add base Makefile" && \
    jj new && \
    printf 'all:\n\techo done\nlint:\n\tpylint src/\n' > Makefile && \
    jj describe -m "build: add lint target" && \
    jj new && \
    printf 'all:\n\techo done\nlint:\n\tpylint --errors-only src/\n' > Makefile && \
    jj describe -m "wip: fixup lint flag"

# Container contents:
#   - /home/user/monorepo — jj repo with 3 commits above root
#       1. "build: add base Makefile"
#       2. "build: add lint target"
#       3. "wip: fixup lint flag" @ (Makefile with --errors-only)

CMD ["/bin/bash"]
