FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo configured for GPG commit signing with pre-generated GPG key for signing@example.com."

RUN mkdir -p /home/user/.gnupg && \
    chmod 700 /home/user/.gnupg

ENV GNUPGHOME=/home/user/.gnupg

RUN cat > /home/user/gpg-batch <<'INEOF'
%echo Generating a basic OpenPGP key
Key-Type: RSA
Key-Length: 2048
Subkey-Type: RSA
Subkey-Length: 2048
Name-Real: Signing User
Name-Email: signing@example.com
Expire-Date: 0
%no-protection
%commit
%echo done
INEOF

RUN gpg --batch --generate-key /home/user/gpg-batch && \
    gpgconf --kill gpg-agent || true

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Signing User" && \
    jj config set --repo user.email "signing@example.com"

RUN echo 'export GPG_TTY=$(tty)' >> /home/user/.bashrc

# Container contents:
#   - /home/user/repo  — newly initialized jj repository
#   - /home/user/.gnupg — GPG keyring containing key for signing@example.com
#   - Python 3, pip, pytest, and gnupg available for automated verification.

CMD ["/bin/bash"]
