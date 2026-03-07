FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: prune stale audit revisions using revsets and jj abandon"

# Install system dependencies and Python test tooling
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        git \
        python3 \
        python3-pip \
        bash && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install jj binary
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Bootstrap the repository state
ENV EDITOR=true

RUN jj config set --user user.name "Audit Bot" && \
    jj config set --user user.email "audit@acme.corp"

RUN mkdir -p /home/user/audit-repo && \
    cd /home/user/audit-repo && \
    jj git init .

RUN cd /home/user/audit-repo && \
    jj config set --repo user.name "Audit Bot" && \
    jj config set --repo user.email "audit@acme.corp"

# Commit 1: init: scaffold audit repo
RUN cd /home/user/audit-repo && \
    echo "# Audit Repo" > README.md && \
    jj describe -m "init: scaffold audit repo" && \
    jj new

# Commit 2: feat: add ingestion pipeline
RUN cd /home/user/audit-repo && \
    mkdir -p pipelines && \
    echo "# ingest pipeline" > pipelines/ingest.py && \
    jj describe -m "feat: add ingestion pipeline" && \
    jj new

# Commit 3: feat: add transformation step
RUN cd /home/user/audit-repo && \
    echo "# transform step" > pipelines/transform.py && \
    jj describe -m "feat: add transformation step" && \
    jj new

# Commit 4: draft: WIP validation logic (do not merge)
RUN cd /home/user/audit-repo && \
    echo "# wip validation" > pipelines/validate_wip.py && \
    jj describe -m "draft: WIP validation logic (do not merge)" && \
    jj new

# Commit 5: draft: experimental dedup pass
RUN cd /home/user/audit-repo && \
    echo "# experimental dedup" > pipelines/dedup_exp.py && \
    jj describe -m "draft: experimental dedup pass" && \
    jj new

# Commit 6: feat: add reporting module + create audit-main bookmark + advance working copy
RUN cd /home/user/audit-repo && \
    mkdir -p reports && \
    echo "# reporting" > reports/summary.py && \
    jj describe -m "feat: add reporting module" && \
    jj bookmark create audit-main -r @ && \
    jj new

# Container contents:
#   /home/user/audit-repo  — jj git-backed repository
#   Revisions (oldest -> newest):
#     1. init: scaffold audit repo         (README.md)
#     2. feat: add ingestion pipeline      (pipelines/ingest.py)
#     3. feat: add transformation step     (pipelines/transform.py)
#     4. draft: WIP validation logic       (pipelines/validate_wip.py)
#     5. draft: experimental dedup pass    (pipelines/dedup_exp.py)
#     6. feat: add reporting module        (reports/summary.py)  <-- audit-main
#     7. (empty working copy @ on top of 6)
#   Task: abandon draft:* revisions, move audit-main bookmark to cleaned tip

CMD ["/bin/bash"]
