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
LABEL Description="jj repo at /home/user/release-repo with 6 commits by 3 authors for changelog generation and v1.1 release task."

# Configure global identity
RUN jj config set --user user.name "Release Manager" && \
    jj config set --user user.email "release@example.com"

# Initialize repo with v1.0 baseline
RUN jj git init /home/user/release-repo && \
    cd /home/user/release-repo && \
    jj config set --repo user.name "Release Manager" && \
    jj config set --repo user.email "release@example.com" && \
    printf '# Release Repo\n' > README.md && \
    jj describe -m "release: v1.0 baseline" && \
    jj bookmark create v1.0 -r @

# Commit 1: feat: new dashboard UI (Alice)
RUN cd /home/user/release-repo && \
    jj new && \
    mkdir -p src && \
    printf 'def render_dashboard():\n    return "dashboard"\n' > src/dashboard.py && \
    jj describe -m "feat: new dashboard UI" --author "Alice <alice@company.com>"

# Commit 2: fix: correct login redirect (Bob)
RUN cd /home/user/release-repo && \
    jj new && \
    printf 'def login_redirect(user):\n    return "/dashboard"\n' > src/auth.py && \
    jj describe -m "fix: correct login redirect" --author "Bob <bob@company.com>"

# Commit 3: feat: add CSV export (Alice)
RUN cd /home/user/release-repo && \
    jj new && \
    printf 'def export_csv(data):\n    return ",".join(str(x) for x in data)\n' > src/export.py && \
    jj describe -m "feat: add CSV export" --author "Alice <alice@company.com>"

# Commit 4: fix: prevent XSS in user input (Charlie)
RUN cd /home/user/release-repo && \
    jj new && \
    printf 'def sanitize(text):\n    return text.replace("<", "&lt;").replace(">", "&gt;")\n' > src/input_sanitizer.py && \
    jj describe -m "fix: prevent XSS in user input" --author "Charlie <charlie@company.com>"

# Commit 5: chore: update dependencies (Bob)
RUN cd /home/user/release-repo && \
    jj new && \
    printf 'flask==3.0.0\nrequests==2.31.0\n' > requirements.txt && \
    jj describe -m "chore: update dependencies" --author "Bob <bob@company.com>"

# Commit 6: feat: add dark mode (Charlie)
RUN cd /home/user/release-repo && \
    jj new && \
    printf 'def get_theme(mode="light"):\n    return {"background": "#000" if mode == "dark" else "#fff"}\n' > src/theme.py && \
    jj describe -m "feat: add dark mode" --author "Charlie <charlie@company.com>" && \
    jj bookmark create main -r @

# Container contents:
#   /home/user/release-repo — jj repo with:
#     v1.0 bookmark: "release: v1.0 baseline"
#     main bookmark: "feat: add dark mode" (6 commits above v1.0 by Alice/Bob/Charlie)

CMD ["/bin/bash"]
