FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (adjust version as needed)
RUN curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-24.0.2.tgz | tar xz --strip 1 -C /usr/local/bin docker/docker

RUN docker --version

USER jenkins
