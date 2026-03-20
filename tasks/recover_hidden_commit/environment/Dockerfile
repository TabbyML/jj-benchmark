FROM ubuntu:22.04

LABEL Author="jj-task-builder"

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

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV EDITOR=true
ENV JJ_USER="Test User"
ENV JJ_EMAIL="test@example.com"

# Initialize jj repo
RUN jj git init /home/user/kernel-patch

WORKDIR /home/user/kernel-patch

RUN jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

# Create watchdog commit on top of root (WC starts at root)
RUN printf '/* watchdog timer implementation */\n' > watchdog.c && \
    jj describe -m "feat: add watchdog timer support"

# Save watchdog commit ID for later use in abandon step
# Create a new branch from root for main chain
RUN jj new 'root()'

# Build main chain: init: add initial Makefile
RUN echo "all: build" > Makefile && \
    jj describe -m "init: add initial Makefile" && \
    jj new

# Add irq.c commit
RUN printf '/* interrupt handler */\nvoid handle_irq(void) {}\n' > irq.c && \
    jj describe -m "refactor: clean up interrupt handler" && \
    jj new

# Save the current WC change ID, then abandon the watchdog commit
RUN WC_ID=$(jj log -r @ --no-graph -T 'change_id') && \
    WATCHDOG_ID=$(jj log -r 'description(substring:"watchdog")' --no-graph -T 'change_id') && \
    jj abandon "$WATCHDOG_ID" && \
    CURRENT_WC=$(jj log -r @ --no-graph -T 'change_id') && \
    if [ "$CURRENT_WC" != "$WC_ID" ]; then jj edit "$WC_ID"; fi

CMD ["/bin/bash"]
