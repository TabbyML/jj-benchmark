FROM ubuntu:22.04

# Install basic tools and Python for testing
RUN apt-get update && apt-get install -y curl tar git python3 && rm -rf /var/lib/apt/lists/*

# Install Jujutsu
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

# Create user
RUN useradd -m -s /bin/bash user
USER user
WORKDIR /home/user

# Configure Jujutsu
RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Setup the repository
RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init && \
    jj new -m "Add feature 1" && \
    echo "content1" > feature1.txt && \
    jj new -m "Add feature 2" && \
    echo "content2" > feature2.txt && \
    jj new -m "Add feature 3" && \
    echo "content3" > feature3.txt && \
    jj new

CMD ["/bin/bash"]
