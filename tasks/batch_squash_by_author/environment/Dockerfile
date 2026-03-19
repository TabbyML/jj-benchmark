FROM ubuntu:24.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip python3-pytest bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj config set --user user.name "Test User" && jj config set --user user.email "test@example.com"

WORKDIR /home/user

RUN jj git init repo

WORKDIR /home/user/repo

# Commit 1: human user (Test User)
RUN echo "initial data" > data.txt && \
    jj describe -m "feat: initial data setup"

# Switch to bot user for commits 2-4
RUN jj config set --user user.name "Bot User" && \
    jj config set --user user.email "bot@company.com"

# Commit 2: bot
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 1" >> data.txt && \
    jj describe -m "chore: automated lint fix 1"

# Commit 3: bot (consecutive)
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 2" >> data.txt && \
    jj describe -m "chore: automated lint fix 2"

# Commit 4: bot (consecutive)
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 3" >> data.txt && \
    jj describe -m "chore: automated format fix 1"

# Switch back to human user for commit 5
RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Commit 5: human
RUN jj new && \
    echo "# main module" > main.py && \
    jj describe -m "feat: add main module"

# Switch to bot user for commits 6-7
RUN jj config set --user user.name "Bot User" && \
    jj config set --user user.email "bot@company.com"

# Commit 6: bot
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 4" >> data.txt && \
    jj describe -m "chore: automated lint fix 3"

# Commit 7: bot (consecutive)
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 5" >> data.txt && \
    jj describe -m "chore: automated format fix 2"

# Switch back to human for commit 8
RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Commit 8: human
RUN jj new && \
    echo "def process(): pass" >> main.py && \
    jj describe -m "feat: add process function"

# Switch to bot for commits 9-11
RUN jj config set --user user.name "Bot User" && \
    jj config set --user user.email "bot@company.com"

# Commit 9: bot
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 6" >> data.txt && \
    jj describe -m "chore: automated lint fix 4"

# Commit 10: bot (consecutive)
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 7" >> data.txt && \
    jj describe -m "chore: automated lint fix 5"

# Commit 11: bot (consecutive)
RUN jj new && \
    jj metaedit --update-author && \
    echo "bot change 8" >> data.txt && \
    jj describe -m "chore: automated format fix 3"

# Switch back to human for commit 12
RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Commit 12: human
RUN jj new && \
    echo "def cleanup(): pass" >> main.py && \
    jj describe -m "feat: add cleanup function"

RUN jj bookmark create main -r @

CMD ["/bin/bash"]
