FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.28.1/jj-v0.28.1-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="Colocated jj+git repo with 5-commit patch series to be exported as email-format patches."

RUN jj config set --user user.name "Contributor" && \
    jj config set --user user.email "contrib@example.com" && \
    git config --global user.name "Contributor" && \
    git config --global user.email "contrib@example.com" && \
    git config --global init.defaultBranch main

# Initialize repo with base content
RUN git init /home/user/patch-work && \
    cd /home/user/patch-work && \
    mkdir -p src tests docs && \
    printf 'def parse(tokens):\n    result = []\n    for i in range(len(tokens) - 1):  # off-by-one bug here\n        result.append(tokens[i])\n    return result\n' > src/parser.py && \
    printf 'def tokenize(text):\n    return text.split()\n' > src/tokenizer.py && \
    printf 'def test_parser_basic():\n    pass\n' > tests/test_parser.py && \
    printf '# Parser\nBasic parser module.\n' > docs/parser.md && \
    git add src/ tests/ docs/ && \
    git commit -m "chore: initial parser implementation" && \
    jj git init --colocate && \
    jj config set --repo user.name "Contributor" && \
    jj config set --repo user.email "contrib@example.com"

# Commit 1: fix off-by-one error
RUN cd /home/user/patch-work && \
    jj new main && \
    printf 'def parse(tokens):\n    result = []\n    for i in range(len(tokens)):  # fixed off-by-one\n        result.append(tokens[i])\n    return result\n' > src/parser.py && \
    jj describe -m "fix: correct off-by-one error in parser"

# Commit 2: handle empty input in tokenizer
RUN cd /home/user/patch-work && \
    jj new && \
    printf 'def tokenize(text):\n    if not text:\n        return []\n    return text.split()\n' > src/tokenizer.py && \
    jj describe -m "fix: handle empty input in tokenizer"

# Commit 3: extract validation helper
RUN cd /home/user/patch-work && \
    jj new && \
    printf 'def validate_tokens(tokens):\n    """Validate that tokens list is non-empty and contains strings."""\n    if not tokens:\n        raise ValueError("Token list cannot be empty")\n    for t in tokens:\n        if not isinstance(t, str):\n            raise TypeError(f"Token must be string, got {type(t)}")\n    return True\n' > src/validation.py && \
    jj describe -m "refactor: extract validation helper"

# Commit 4: add parser edge case tests
RUN cd /home/user/patch-work && \
    jj new && \
    printf 'from src.parser import parse\nfrom src.tokenizer import tokenize\nfrom src.validation import validate_tokens\n\ndef test_parser_basic():\n    tokens = ["a", "b", "c"]\n    assert parse(tokens) == ["a", "b", "c"]\n\ndef test_tokenizer_empty():\n    assert tokenize("") == []\n\ndef test_tokenizer_whitespace():\n    assert tokenize("  ") == []\n\ndef test_validation_empty_raises():\n    try:\n        validate_tokens([])\n        assert False, "Should raise ValueError"\n    except ValueError:\n        pass\n' > tests/test_parser.py && \
    jj describe -m "test: add parser edge case tests"

# Commit 5: update docs
RUN cd /home/user/patch-work && \
    jj new && \
    printf '# Parser Module\n\n## Overview\nThis module provides parsing and tokenization utilities.\n\n## Functions\n\n### `parse(tokens)`\nParses a list of tokens into a result list.\n\n### `tokenize(text)`\nConverts a text string to a list of tokens. Returns empty list for empty input.\n\n### `validate_tokens(tokens)`\nValidates that a token list is valid (non-empty, all strings).\n' > docs/parser.md && \
    jj describe -m "docs: update parser documentation" && \
    jj bookmark create patch-series -r @

# Container state:
#   /home/user/patch-work — colocated jj+git repo with 5-commit patch series
#     main: "chore: initial parser implementation"
#     patch-series: tip of 5-commit stack

CMD ["/bin/bash"]