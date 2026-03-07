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
LABEL Description="jj repo with main, dev, and feature bookmarks, where feature is mistakenly rebased onto dev."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "main content" > main.txt && \
    jj describe -m "main commit" && \
    jj bookmark create main && \
    jj new main && \
    echo "feature parent content" > feature_parent.txt && \
    jj describe -m "feature parent" && \
    FEATURE_PARENT=$(jj log --no-graph -T 'commit_id' -r @) && \
    jj new main && \
    echo "dev content" > dev.txt && \
    jj describe -m "dev commit" && \
    jj bookmark create dev && \
    jj new "$FEATURE_PARENT" && \
    echo "feature content" > feature.txt && \
    jj describe -m "feature commit" && \
    jj bookmark create feature && \
    jj rebase -b feature -d dev

# Container contents:
#   - /home/user/repo  — jj repository with:
#       - main bookmark pointing to "main commit"
#       - dev bookmark pointing to "dev commit"
#       - feature bookmark pointing to "feature commit" (mistakenly rebased onto dev)
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
