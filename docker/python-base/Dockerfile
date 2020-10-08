FROM python:3.8-alpine

# Install Docker
RUN apk update \
    && apk add wget \
    && apk add dumb-init

RUN pip install pipenv

# Install Watchman - https://github.com/facebook/watchman/releases
RUN wget "https://github.com/facebook/watchman/releases/download/v2020.09.21.00/watchman-v2020.09.21.00-linux.zip" --output-document="watchman.zip"
RUN unzip "watchman.zip"
RUN mkdir -p /usr/local/{bin,lib} /usr/local/var/run/watchman
RUN cp -r watchman-v2020.09.21.00-linux/bin/* /usr/local/bin
RUN cp -r watchman-v2020.09.21.00-linux/lib/* /usr/local/lib
RUN chmod 755 /usr/local/bin/watchman
RUN chmod 2777 /usr/local/var/run/watchman
