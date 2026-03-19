FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL description="jj task: squash, split, and amend commits for release branch preparation"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -sSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin/ ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV EDITOR=true

# Configure jj global identity
RUN jj config set --user user.name "Release Manager" && \
    jj config set --user user.email "release@example.com"

# Create the repo and initial structure
RUN mkdir -p /home/user/widget-engine/src

WORKDIR /home/user/widget-engine

RUN jj git init --no-colocate .

RUN jj config set --repo user.name "Release Manager" && \
    jj config set --repo user.email "release@example.com"

# Commit 1: initial project scaffold
RUN printf '# api.py - placeholder\n' > /home/user/widget-engine/src/api.py && \
    printf '# auth.py - placeholder\n' > /home/user/widget-engine/src/auth.py && \
    jj describe -m "initial project scaffold" && \
    jj new

# Commit 2: add API endpoint and fix login bug (mixed commit)
RUN printf '# api.py - widget engine API\ndef get_widget(widget_id):\n    """Return a widget by ID."""\n    return {"id": widget_id, "name": "Widget " + str(widget_id)}\n\ndef create_widget(name):\n    """Create a new widget."""\n    return {"id": 1, "name": name}\n' > /home/user/widget-engine/src/api.py && \
    printf '# auth.py - widget engine authentication\ndef login(username, password):\n    """Authenticate a user. Fixed: now checks password correctly."""\n    if not username or not password:\n        raise ValueError("Username and password are required")\n    return username == "admin" and password == "secret"\n' > /home/user/widget-engine/src/auth.py && \
    jj describe -m "add API endpoint and fix login bug" && \
    jj new

# Commit 3: add release notes
RUN printf '# Widget Engine v2.3.0 Release Notes\n\n## New Features\n- New REST API endpoint for widget retrieval and creation\n\n## Bug Fixes\n- Fixed login authentication to properly validate credentials\n' > /home/user/widget-engine/RELEASE_NOTES.md && \
    jj describe -m "add release notes" && \
    jj new

# Commit 4: wip: bump version
RUN printf '2.3.0\n' > /home/user/widget-engine/version.txt && \
    jj describe -m "wip: bump version" && \
    jj new

# Commit 5: fixup: missing newline in release notes
RUN printf '\n' >> /home/user/widget-engine/RELEASE_NOTES.md && \
    jj describe -m "fixup: missing newline in release notes" && \
    jj bookmark create release/v2.3 -r @ && \
    jj new

CMD ["/bin/bash"]
