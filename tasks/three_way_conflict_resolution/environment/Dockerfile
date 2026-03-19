FROM ubuntu:24.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip python3-pytest bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV HOME=/home/user

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Initialize the repository
RUN jj git init /home/user/repo

WORKDIR /home/user/repo

# Create base commit with src/config.py
RUN mkdir -p src && \
    printf '# Configuration file\nDATABASE_HOST = "localhost"\nDATABASE_PORT = 5432\nDATABASE_NAME = "mydb"\nLOG_LEVEL = "INFO"\nMAX_CONNECTIONS = 10\nTIMEOUT = 30\n' > src/config.py && \
    jj describe -m "base: initial config" && \
    jj bookmark create base -r @

# Create branch-a: modifies DATABASE settings
RUN jj new base -m "branch-a: update database config" && \
    printf '# Configuration file\nDATABASE_HOST = "db.production.example.com"\nDATABASE_PORT = 5433\nDATABASE_NAME = "mydb_prod"\nLOG_LEVEL = "INFO"\nMAX_CONNECTIONS = 50\nTIMEOUT = 30\n' > src/config.py && \
    jj bookmark create branch-a -r @

# Create branch-b: modifies LOG and TIMEOUT settings
RUN jj new base -m "branch-b: update logging and timeout" && \
    printf '# Configuration file\nDATABASE_HOST = "localhost"\nDATABASE_PORT = 5432\nDATABASE_NAME = "mydb"\nLOG_LEVEL = "DEBUG"\nMAX_CONNECTIONS = 10\nTIMEOUT = 60\n' > src/config.py && \
    jj bookmark create branch-b -r @

# Create the merge commit - this will have conflicts
RUN jj new branch-a branch-b -m "merge-ab: merge branch-a and branch-b" && \
    jj bookmark create merge-ab -r @

CMD ["/bin/bash"]
