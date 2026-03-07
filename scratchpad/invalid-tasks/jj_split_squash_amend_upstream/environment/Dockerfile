FROM ubuntu:22.04

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

RUN mkdir -p /home/user/.config/jj
RUN cat > /home/user/.config/jj/config.toml <<'EOF'
[user]
name = "Test Contributor"
email = "contributor@example.com"

[ui]
editor = "true"
EOF

ENV HOME=/home/user

RUN mkdir -p /home/user/myproject/src

WORKDIR /home/user/myproject

RUN jj git init --colocate .

RUN cat > /home/user/myproject/README.md <<'EOF'
# myproject

A sample project.
EOF

RUN cat > /home/user/myproject/Cargo.toml <<'EOF'
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"
EOF

RUN jj describe -m "init: scaffold project structure" && jj new

RUN cat > /home/user/myproject/src/parser.rs <<'EOF'
pub fn parse(input: &str) -> Vec<&str> {
    input.split_whitespace().collect()
}
EOF

RUN cat > /home/user/myproject/src/http.rs <<'EOF'
pub fn get(url: &str) -> String {
    format!("GET {}", url)
}
EOF

RUN cat > /home/user/myproject/src/lib.rs <<'EOF'
pub mod parser;
pub mod http;

fn debug_helper() {
    println!("debug: http module loaded");
}
EOF

RUN jj describe -m "add parser and http client" && jj new

RUN cat > /home/user/myproject/src/lib.rs <<'EOF'
pub mod parser;
pub mod http;
EOF

RUN jj describe -m "fix: forgot to remove debug print" && jj new

LABEL Author="jj-task-builder"

CMD ["/bin/bash"]
