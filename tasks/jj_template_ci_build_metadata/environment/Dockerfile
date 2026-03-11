FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com"

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN jj git init --colocate /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'project: ci-demo\n' > README.md && \
    jj describe -m "init: project setup" && \
    jj bookmark create main -r @ && \
    jj new

RUN cd /home/user/repo && \
    mkdir -p src && \
    printf 'def run():\n    print("running")\n' > src/main.py && \
    jj describe -m "feat: initial implementation" && \
    jj new

RUN cd /home/user/repo && \
    printf 'def test_run():\n    assert True\n' > src/test_main.py && \
    jj describe -m "test: add basic tests" && \
    jj new

RUN cd /home/user/repo && \
    mkdir -p .github/workflows && \
    printf 'name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n' > .github/workflows/ci.yml && \
    printf '#!/bin/bash\nset -e\npython3 -m pytest src/\n' > build.sh && \
    chmod +x build.sh && \
    jj describe -m "feat: add build pipeline"

LABEL Description="jj repo with build pipeline commit for CI metadata extraction task"

CMD ["/bin/bash"]
