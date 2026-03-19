FROM ubuntu:24.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip python3-pytest bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV HOME=/home/user

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com"

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN jj git init /home/user/repo

WORKDIR /home/user/repo

# Commit 1: add parser.py
RUN printf 'def parse(data):\n    return data.split(",")\n' > parser.py && \
    jj describe -m "commit-1: add parser" && \
    jj bookmark create commit-1 -r @

# Commit 2: add validator.py
RUN jj new commit-1 -m "commit-2: add validator" && \
    printf 'def validate(items):\n    return [i for i in items if i]\n' > validator.py && \
    jj bookmark create commit-2 -r @

# Commit 3: add formatter.py
RUN jj new commit-2 -m "commit-3: add formatter" && \
    printf 'def format_output(items):\n    return ", ".join(items)\n' > formatter.py && \
    jj bookmark create commit-3 -r @

# Commit 4: add exporter.py
RUN jj new commit-3 -m "commit-4: add exporter" && \
    printf 'def export(data, path):\n    open(path, "w").write(data)\n' > exporter.py && \
    jj bookmark create commit-4 -r @

# Commit 5: add runner.py
RUN jj new commit-4 -m "commit-5: add runner" && \
    printf 'def run(input_data):\n    return input_data.strip()\n' > runner.py && \
    jj bookmark create commit-5 -r @

# Now create the working copy with fixups for commits 1, 3, and 5
# Fixup for commit-1: improve parser to handle whitespace
# Fixup for commit-3: improve formatter to handle empty items
# Fixup for commit-5: improve runner to handle None
RUN jj new commit-5 -m "wip: fixups for parser, formatter, and runner" && \
    printf 'def parse(data):\n    return [item.strip() for item in data.split(",")]\n' > parser.py && \
    printf 'def format_output(items):\n    return ", ".join(str(i) for i in items if i)\n' > formatter.py && \
    printf 'def run(input_data):\n    if input_data is None:\n        return ""\n    return input_data.strip()\n' > runner.py

CMD ["/bin/bash"]
