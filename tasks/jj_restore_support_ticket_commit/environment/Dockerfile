FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: recover an abandoned support ticket commit via op log and jj new"

ENV DEBIAN_FRONTEND=noninteractive
ENV EDITOR=true

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN mkdir -p /home/user/support-repo

RUN jj git init /home/user/support-repo

RUN jj -R /home/user/support-repo config set --repo user.name "Support Engineer"
RUN jj -R /home/user/support-repo config set --repo user.email "support@example.com"

RUN echo "# Support Repository" > /home/user/support-repo/README.md && \
    jj -R /home/user/support-repo describe -m "initial project setup"

RUN jj -R /home/user/support-repo bookmark create main -r @

RUN jj -R /home/user/support-repo new -m "fix: null pointer in auth service (ticket-1042)"

RUN cat > /home/user/support-repo/auth_fix.py << 'EOF'
# Auth service null pointer fix for ticket-1042
# The original code did not guard against None user objects.


def get_user_roles(user):
    """Return the roles for a user, guarding against None."""
    if user is None:
        return []
    return user.roles


def authenticate(request):
    """Authenticate an incoming request.

    Fixes null pointer exception when request.user is not set.
    """
    user = getattr(request, "user", None)
    roles = get_user_roles(user)
    return len(roles) > 0
EOF

RUN jj -R /home/user/support-repo new

RUN jj -R /home/user/support-repo abandon @-

CMD ["/bin/bash"]
