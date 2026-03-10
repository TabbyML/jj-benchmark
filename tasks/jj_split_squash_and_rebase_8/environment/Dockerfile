FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with a messy feature branch needing split and squash operations."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new && \
    jj describe -m "add utils.py" && \
    echo "def helper(): return True" > utils.py && \
    jj new && \
    jj describe -m "mixed changes" && \
    echo "def helper(): return False" > utils.py && \
    echo "def api_func(): return 'api'" > api.py && \
    jj new && \
    jj describe -m "add tests" && \
    echo "def test_api(): assert api_func() == 'api'" > test_api.py && \
    jj bookmark create feature -r @

# Container contents:
#   - /home/user/repo  — jj repository with a main branch and a feature branch
#       - "Initial commit" (main)
#       - "add utils.py" (creates utils.py)
#       - "mixed changes" (modifies utils.py, creates api.py)
#       - "add tests" (creates test_api.py, tagged with feature bookmark)
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
