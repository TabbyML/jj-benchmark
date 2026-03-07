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
LABEL Description="jj repo with a stack of commits on feature-stack branch in /home/user/workspace/repo."

RUN mkdir -p /home/user/workspace && \
    jj git init /home/user/workspace/repo && \
    cd /home/user/workspace/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "# README" > README.md && \
    jj describe -m "Initial commit with README.md" && \
    jj bookmark create main && \
    jj new && \
    echo "def feature_a():" > feature_a.py && \
    echo "    print('initial code')" >> feature_a.py && \
    jj describe -m "Add feature A" && \
    jj new && \
    echo "def feature_a():" > feature_a.py && \
    echo "    print('initial code with bug')" >> feature_a.py && \
    echo "def feature_b():" > feature_b.py && \
    echo "    print('feature b')" >> feature_b.py && \
    jj describe -m "Update feature A and add feature B" && \
    jj new && \
    echo "def feature_a():" > feature_a.py && \
    echo "    print('initial code with fix')" >> feature_a.py && \
    jj describe -m "Fix typo in feature A" && \
    jj bookmark create feature-stack

# Container contents:
#   - /home/user/workspace/repo  — jj repository with:
#       - A `main` bookmark pointing to an initial commit
#       - A `feature-stack` bookmark pointing to a stack of 3 commits
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
