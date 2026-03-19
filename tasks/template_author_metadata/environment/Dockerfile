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
LABEL Description="jj repo with 3 commits by different authors in /home/user/repo."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Alice" && \
    jj config set --repo user.email "alice@example.com" && \
    echo "feature code" > feature.txt && \
    jj describe -m "Add new feature" && \
    jj new && \
    jj config set --repo user.name "Bob" && \
    jj config set --repo user.email "bob@example.com" && \
    echo "bug fix code" > bugfix.txt && \
    jj describe -m "Fix a critical bug" && \
    jj new && \
    jj config set --repo user.name "Charlie" && \
    jj config set --repo user.email "charlie@example.com" && \
    echo "docs update" > docs.txt && \
    jj describe -m "Update documentation"

# Container contents:
#   - /home/user/repo  — jj repository with three commits above root:
#       - "Add new feature" by Alice
#       - "Fix a critical bug" by Bob
#       - "Update documentation" by Charlie
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
