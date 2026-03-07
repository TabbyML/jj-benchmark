FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="Task environment for jj_recover_abandoned_fix_attempt: incident responder recovering an abandoned hotfix commit"

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

# Install jj v0.38.0
RUN curl -sSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Set up the repository environment
RUN jj git init /home/user/repo

RUN jj --repository /home/user/repo config set --repo user.name "Incident Responder" \
    && jj --repository /home/user/repo config set --repo user.email "responder@example.com"

WORKDIR /home/user/repo

# Create initial scaffold commit
RUN mkdir -p src/payments \
    && echo "# payments service" > src/payments/__init__.py \
    && jj describe -m "feat: initial payments service scaffold" \
    && jj new

# Create invoice generation commit
RUN echo "# invoice generation module" > src/payments/invoice.py \
    && jj describe -m "feat: add invoice generation" \
    && jj new

# Capture change IDs and create + abandon the fix commit
RUN SCAFFOLD_ID=$(jj log --no-pager --no-graph --color never -T 'change_id' -r 'description(substring:"initial payments service scaffold")') \
    && INVOICE_ID=$(jj log --no-pager --no-graph --color never -T 'change_id' -r 'description(substring:"add invoice generation")') \
    && jj new --no-edit "$SCAFFOLD_ID" \
    && FIX_CHANGE_ID=$(jj log --no-pager --no-graph --color never -T 'change_id' -r "children($SCAFFOLD_ID) ~ $INVOICE_ID") \
    && jj edit "$FIX_CHANGE_ID" \
    && mkdir -p src/payments \
    && printf '# Hotfix: round to 2 decimal places\namount = round(amount, 2)\n' > src/payments/billing.py \
    && jj describe -m "fix: billing amount rounding error" \
    && jj abandon "$FIX_CHANGE_ID" \
    && SCAFFOLD_ID=$(jj log --no-pager --no-graph --color never -T 'change_id' -r 'description(substring:"initial payments service scaffold")') \
    && INVOICE_ID=$(jj log --no-pager --no-graph --color never -T 'change_id' -r 'description(substring:"add invoice generation")') \
    && jj bookmark create main -r "$SCAFFOLD_ID" \
    && jj new "$INVOICE_ID"

CMD ["/bin/bash"]
