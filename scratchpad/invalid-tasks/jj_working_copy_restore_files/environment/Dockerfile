FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && pip3 install pytest \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN chmod 0755 /home/user || mkdir -p /home/user && chmod 0755 /home/user

ENV JJ_USER="Incident Responder"
ENV JJ_EMAIL="ir@example.com"

RUN mkdir -p /home/user/incident-repo \
    && cd /home/user/incident-repo \
    && jj git init --no-colocate . \
    && jj config set --repo user.name "Incident Responder" \
    && jj config set --repo user.email "ir@example.com"

RUN cd /home/user/incident-repo \
    && mkdir -p src config \
    && printf '# Incident Repo\n\nExample project for incident response exercises.\n' > README.md \
    && printf '# src package\n' > src/__init__.py \
    && printf '# config package\n' > config/__init__.py \
    && jj describe -m "init: project scaffold" \
    && jj new

RUN cd /home/user/incident-repo \
    && printf '[app]\nname = "incident-service"\nversion = "1.0.0"\ndebug = false\n\n[database]\nhost = "localhost"\nport = 5432\nname = "incidents_db"\nuser = "svc_user"\n' > config/settings.toml \
    && jj describe -m "feat: add config module" \
    && jj new

RUN cd /home/user/incident-repo \
    && printf '"""Metrics collection module."""\n\n\ndef collect_metrics():\n    """Collect system metrics and return a dict."""\n    return {\n        "cpu_usage": 0.0,\n        "memory_usage": 0.0,\n        "request_count": 0,\n    }\n\n\ndef push_metrics(metrics: dict) -> bool:\n    """Push metrics to the monitoring backend."""\n    if not metrics:\n        return False\n    # TODO: implement actual push\n    return True\n' > src/metrics.py \
    && printf '[app]\nname = "incident-service"\nversion = "1.0.0"\ndebug = false\n\n[database]\nhost = "localhost"\nport = 5432\nname = "incidents_db"\nuser = "svc_user"\n\n[metrics]\nendpoint = "http://metrics.internal/push"\ninterval_sec = 30\n' > config/settings.toml \
    && jj describe -m "wip: integrate metrics module"

RUN cd /home/user/incident-repo \
    && printf 'DEBUG_GARBAGE: this file was corrupted during an interrupted edit session\nprint(undefined_var)  # accidental debug output\nx = [1, 2, 3\n# incomplete bracket -- syntax error\n' > src/metrics.py \
    && printf '[app]\nname = "incident-service"\nversion = "1.0.0"\ndebug = false\n\nCORRUPTED: the database section was accidentally deleted during edit\n\n[metrics]\nendpoint = "http://metrics.internal/push"\ninterval_sec = 30\n' > config/settings.toml \
    && jj status --no-pager > /dev/null

CMD ["/bin/bash"]
