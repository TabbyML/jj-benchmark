FROM jj-task-base:latest

RUN mkdir -p /home/user/wc-marker-repo /home/user/.config/jj

RUN printf '[user]\nname = "Test User"\nemail = "test@example.com"\n' > /home/user/.config/jj/config.toml

ENV JJ_CONFIG=/home/user/.config/jj/config.toml

RUN jj git init /home/user/wc-marker-repo && \
    cd /home/user/wc-marker-repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN printf 'one\n' > /home/user/wc-marker-repo/one.txt && \
    cd /home/user/wc-marker-repo && jj describe -m "feat: first commit" && jj new

RUN printf 'two\n' > /home/user/wc-marker-repo/two.txt && \
    cd /home/user/wc-marker-repo && jj describe -m "feat: second commit" && jj new

RUN printf 'three\n' > /home/user/wc-marker-repo/three.txt && \
    cd /home/user/wc-marker-repo && jj describe -m "feat: third commit" && jj new

LABEL Description="jj repo at /home/user/wc-marker-repo with 3 commits. User must use working_copies template to mark working copy commit in wc_marker_report.txt."

CMD ["/bin/bash"]
