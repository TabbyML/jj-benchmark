FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: split a bundled commit and squash a fixup commit"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Initialize jj git repo
RUN jj git init /home/user/myproject

# Configure jj user identity inside repo
RUN jj --repository /home/user/myproject config set --repo user.name "Dev User" && \
    jj --repository /home/user/myproject config set --repo user.email "dev@example.com"

WORKDIR /home/user/myproject

# Create the bundled commit: add README.md and config.toml
RUN printf '# myproject\n\nWellcome to myproject\n\nThis project does something useful.\n' > README.md && \
    printf '[settings]\ndebug = false\nlog_level = "info"\n' > config.toml && \
    jj describe -m "add README and config" && \
    jj new

# Create fixup commit: correct typo in README
RUN printf '# myproject\n\nWelcome to myproject\n\nThis project does something useful.\n' > README.md && \
    jj describe -m "fixup: correct typo in README" && \
    jj new

CMD ["/bin/bash"]
