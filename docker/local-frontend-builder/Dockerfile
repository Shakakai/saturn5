FROM ubuntu:14.04.3

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

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 0.10.33

# Install nvm with node and npm
# COPY ./nvm_install.sh /nvm_install.sh
# RUN chmod +x /nvm_install.sh
# RUN /nvm_install.sh
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.20.0/install.sh | bash
RUN . $NVM_DIR/nvm.sh

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/v$NODE_VERSION/bin:$PATH

COPY ./builder.sh /start
RUN chmod +x /start

ENTRYPOINT ["/bin/bash", "-c", "/start"]
