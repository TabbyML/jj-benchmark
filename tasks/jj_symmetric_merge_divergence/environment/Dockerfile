FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Initialize repo
RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    git init && \
    git config user.name "Test User" && \
    git config user.email "test@example.com" && \
    jj git init --colocate && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

# Create main base commit
RUN cd /home/user/repo && \
    mkdir -p src && \
    printf '# Main application\nAPP_VERSION = "1.0.0"\n' > src/app.py && \
    printf '# Patch module\n\ndef placeholder():\n    pass\n' > src/patch.py && \
    jj describe -m "chore: initial setup" && \
    jj bookmark create main -r @

# Create patch-v1 commit (first divergent version)
RUN cd /home/user/repo && \
    jj new main -m "fix: patch" && \
    printf '# Patch module\n\n\ndef apply_patch_v1():\n    """Apply patch version 1."""\n    return "patch_v1"\n' > src/patch.py && \
    jj bookmark create patch -r @ && \
    jj bookmark create patch-v1-ref -r @

# Create patch-v2 commit (second divergent version — different child of main)
RUN cd /home/user/repo && \
    jj new main -m "fix: patch" && \
    printf '# Patch module\n\n\ndef apply_patch_v2():\n    """Apply patch version 2."""\n    return "patch_v2"\n' > src/patch.py && \
    jj bookmark create patch-v2-ref -r @

# Leave at neutral working copy
RUN cd /home/user/repo && \
    jj new -m "wip: workspace" && \
    echo "=== Divergent commits ===" && \
    jj log --no-graph -T 'change_id ++ " " ++ description ++ "\n"' -r 'description("fix: patch")'

WORKDIR /home/user/repo
CMD ["/bin/bash"]
