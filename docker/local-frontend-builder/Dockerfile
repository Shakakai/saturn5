FROM ubuntu:14.04.3

ARG NODE_VERSION=14

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set debconf to run non-interactively
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install base dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Install Node & Yarn
RUN curl -sL https://deb.nodesource.com/setup_${NODE_VERSION}.x | sudo -E bash -
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y -q yarn nodejs

# Setup the startup script
COPY ./builder.sh /start
RUN chmod +x /start

ENTRYPOINT ["/bin/bash", "-c", "/start"]
