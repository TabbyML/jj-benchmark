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
LABEL Description="jj repo at /home/user/audit-repo with 5 commits: chore: add pipeline config, feat: add transform script, wip: debug temp, feat: add validation logic, wip: scratch notes; task is to abandon wip revisions using revsets."

RUN mkdir -p /home/user/audit-repo && \
    cd /home/user/audit-repo && \
    jj git init . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    printf '[pipeline]\nversion = 1\n' > pipeline_config.toml && \
    jj describe -m "chore: add pipeline config" && \
    jj new && \
    printf 'def transform(data):\n    return [x.strip() for x in data]\n' > transform.py && \
    jj describe -m "feat: add transform script" && \
    jj new && \
    printf 'debug temp\n' > debug.log && \
    jj describe -m "wip: debug temp" && \
    jj new && \
    printf 'def validate(data):\n    return all(len(x) > 0 for x in data)\n' > validation.py && \
    jj describe -m "feat: add validation logic" && \
    jj new && \
    printf 'scratch notes\n' > notes.txt && \
    jj describe -m "wip: scratch notes" && \
    jj new

# Container contents:
#   - /home/user/audit-repo  — jj repository with five commits above root:
#       1. "chore: add pipeline config"   (pipeline_config.toml)
#       2. "feat: add transform script"   (transform.py)
#       3. "wip: debug temp"              (debug.log)
#       4. "feat: add validation logic"   (validation.py)
#       5. "wip: scratch notes"           (notes.txt)
#       6. @ (empty working copy on top of wip: scratch notes)
#   - Task: abandon revisions matching description(glob:"wip:*") and save audit_log.txt

CMD ["/bin/bash"]
