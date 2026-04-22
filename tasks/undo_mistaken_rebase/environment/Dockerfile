FROM pochi-browser-verification-base
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin ./jj && chmod +x /usr/local/bin/jj
RUN mkdir -p /home/user && chmod 0755 /home/user
LABEL Author="any-task-builder"
LABEL Description="jj repo with branches for rebase"
RUN mkdir -p /home/user/repo && cd /home/user/repo && jj git init --colocate && jj config set --user user.name 'Test User' && jj config set --user user.email 'test@example.com' && echo 'base' > f && jj commit -m 'base' && jj bookmark create main && echo 'A' > f && jj commit -m 'A' && jj new main && echo 'B' > f && jj commit -m 'B'
CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
