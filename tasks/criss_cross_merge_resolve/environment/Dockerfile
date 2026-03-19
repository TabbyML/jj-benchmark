FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Set up the criss-cross merge repository
RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    git init && \
    git config user.name "Test User" && \
    git config user.email "test@example.com" && \
    jj git init --colocate && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

# Create initial base commit (main-v1)
RUN cd /home/user/repo && \
    mkdir -p src && \
    printf 'def initialize():\n    pass\n\ndef shutdown():\n    pass\n' > src/core.py && \
    printf 'def format_output(data):\n    return str(data)\n\ndef parse_input(text):\n    return text.strip()\n' > src/utils.py && \
    jj describe -m "chore: initial project structure" && \
    jj new && \
    jj describe -m "chore: main-v1 base"

# Save main-v1 bookmark
RUN cd /home/user/repo && \
    jj bookmark create main-v1 -r @

# Create branch-a initial commit
RUN cd /home/user/repo && \
    jj new main-v1 -m "feat(a): add feature_a module" && \
    printf 'def feature_a_init():\n    """Feature A initialization."""\n    return "feature_a"\n\n\ndef feature_a_run():\n    """Run feature A."""\n    return True\n' > src/feature_a.py && \
    printf 'def initialize():\n    """Initialize the core system with Feature A support."""\n    feature_a_ready = True\n    return feature_a_ready\n\ndef shutdown():\n    pass\n' > src/core.py && \
    printf 'def format_output(data):\n    """Format output with Feature A styling."""\n    return "[A] " + str(data)\n\ndef parse_input(text):\n    return text.strip()\n' > src/utils.py && \
    jj bookmark create branch-a -r @

# Create branch-b initial commit
RUN cd /home/user/repo && \
    jj new main-v1 -m "feat(b): add feature_b module" && \
    printf 'def feature_b_init():\n    """Feature B initialization."""\n    return "feature_b"\n\n\ndef feature_b_run():\n    """Run feature B."""\n    return True\n' > src/feature_b.py && \
    printf 'def initialize():\n    pass\n\ndef shutdown():\n    """Shut down the core system gracefully for Feature B."""\n    feature_b_cleanup = True\n    return feature_b_cleanup\n' > src/core.py && \
    printf 'def format_output(data):\n    return str(data)\n\ndef parse_input(text):\n    """Parse input with Feature B validation."""\n    validated = text.strip().lower()\n    return validated\n' > src/utils.py && \
    jj bookmark create branch-b -r @

# Now create criss-cross: branch-a merges branch-b
RUN cd /home/user/repo && \
    jj new branch-a branch-b -m "merge: branch-b into branch-a (criss)" && \
    printf 'def initialize():\n    """Initialize the core system with Feature A support."""\n    feature_a_ready = True\n    return feature_a_ready\n\ndef shutdown():\n    """Shut down the core system gracefully for Feature B."""\n    feature_b_cleanup = True\n    return feature_b_cleanup\n' > src/core.py && \
    printf 'def format_output(data):\n    """Format output with Feature A styling."""\n    return "[A] " + str(data)\n\ndef parse_input(text):\n    """Parse input with Feature B validation."""\n    validated = text.strip().lower()\n    return validated\n' > src/utils.py && \
    printf 'def feature_a_init():\n    """Feature A initialization."""\n    return "feature_a"\n\n\ndef feature_a_run():\n    """Run feature A."""\n    return True\n' > src/feature_a.py && \
    printf 'def feature_b_init():\n    """Feature B initialization."""\n    return "feature_b"\n\n\ndef feature_b_run():\n    """Run feature B."""\n    return True\n' > src/feature_b.py && \
    jj bookmark move branch-a --to @

# Create branch-b merges branch-a (cross)
RUN cd /home/user/repo && \
    jj new branch-b "branch-a-" -m "merge: branch-a into branch-b (cross)" && \
    printf 'def initialize():\n    """Initialize the core system with Feature A support."""\n    feature_a_ready = True\n    return feature_a_ready\n\ndef shutdown():\n    """Shut down the core system gracefully for Feature B."""\n    feature_b_cleanup = True\n    return feature_b_cleanup\n' > src/core.py && \
    printf 'def format_output(data):\n    """Format output with Feature A styling."""\n    return "[A] " + str(data)\n\ndef parse_input(text):\n    """Parse input with Feature B validation."""\n    validated = text.strip().lower()\n    return validated\n' > src/utils.py && \
    printf 'def feature_a_init():\n    """Feature A initialization."""\n    return "feature_a"\n\n\ndef feature_a_run():\n    """Run feature A."""\n    return True\n' > src/feature_a.py && \
    printf 'def feature_b_init():\n    """Feature B initialization."""\n    return "feature_b"\n\n\ndef feature_b_run():\n    """Run feature B."""\n    return True\n' > src/feature_b.py && \
    jj bookmark move branch-b --to @

# Leave working copy at a neutral position
RUN cd /home/user/repo && \
    jj new -m "wip: workspace" && \
    jj log --no-graph -T 'change_id ++ "\n"' -r 'all()' | head -5

WORKDIR /home/user/repo
CMD ["/bin/bash"]
