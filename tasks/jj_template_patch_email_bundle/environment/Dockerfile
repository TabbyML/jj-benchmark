FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com"

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN jj git init --colocate /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'project: config-parser-lib\n' > README.md && \
    jj describe -m "init: project base" && \
    jj bookmark create main -r @ && \
    jj new

RUN cd /home/user/repo && \
    mkdir -p src && \
    printf 'import tomllib\n\ndef parse_config(path):\n    with open(path, "rb") as f:\n        return tomllib.load(f)\n' > src/config.py && \
    jj describe -m "feat: implement config parser" && \
    jj new

RUN cd /home/user/repo && \
    printf 'def validate_config(cfg):\n    required = ["host", "port"]\n    for key in required:\n        if key not in cfg:\n            raise ValueError(f"Missing required key: {key}")\n    return True\n' > src/validator.py && \
    jj describe -m "feat: add validation layer" && \
    jj new

RUN cd /home/user/repo && \
    printf 'import argparse\n\ndef build_parser():\n    p = argparse.ArgumentParser()\n    p.add_argument("--config", required=True)\n    return p\n' > src/cli.py && \
    jj describe -m "feat: implement CLI interface" && \
    jj new

RUN cd /home/user/repo && \
    printf 'class ConfigError(Exception):\n    def __init__(self, msg, field=None):\n        super().__init__(msg)\n        self.field = field\n' > src/errors.py && \
    jj describe -m "feat: add error reporting" && \
    jj bookmark create feature -r @

RUN cd /home/user/repo && jj new

LABEL Description="jj repo with 4-commit patch series for email bundle generation task"

CMD ["/bin/bash"]
