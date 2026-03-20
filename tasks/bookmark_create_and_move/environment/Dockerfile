FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL description="jj task: create and move bookmarks - developer migrating from Git"

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

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Bootstrap: initialize webapp repo
RUN jj git init /home/user/webapp

# Configure identity
RUN jj --repository /home/user/webapp config set --repo user.name "Dev User"
RUN jj --repository /home/user/webapp config set --repo user.email "dev@example.com"

# Commit 1: root commit
RUN cd /home/user/webapp \
    && mkdir -p app \
    && echo "# Webapp" > README.md \
    && touch app/__init__.py \
    && jj describe -m "chore: init webapp" \
    && jj new

# Commit 2: add homepage route
RUN cd /home/user/webapp \
    && printf 'def homepage():\n    return "Welcome to the homepage!"\n' > app/routes.py \
    && jj describe -m "feat: add homepage route" \
    && jj bookmark create dev -r @ \
    && jj new

# Commit 3: add contact page
RUN cd /home/user/webapp \
    && printf 'def contact():\n    return "Contact us at contact@example.com"\n' > app/contact.py \
    && jj describe -m "feat: add contact page" \
    && jj new

CMD ["/bin/bash"]
