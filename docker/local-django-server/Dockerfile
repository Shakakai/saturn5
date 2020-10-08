FROM python:3.8-alpine

# Install Docker
RUN apk update \
    && apk install -y curl \
    && apk install -y dumb-init

RUN pip install pipenv

# Install Watchman - https://github.com/facebook/watchman/releases
RUN curl "https://github.com/facebook/watchman/releases/download/v2020.09.21.00/watchman-v2020.09.21.00-linux.zip" --output "watchman.zip"
RUN unzip "watchman.zip"
RUN sudo mkdir -p /usr/local/{bin,lib} /usr/local/var/run/watchman
RUN sudo cp bin/* /usr/local/bin
RUN sudo cp lib/* /usr/local/lib
RUN sudo chmod 755 /usr/local/bin/watchman
RUN sudo chmod 2777 /usr/local/var/run/watchman

# Create user and group
RUN addgroup --system django
RUN adduser --system --ingroup django django

# Setup Startup Script
COPY ./startup.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

# Create directory to mount application files
RUN mkdir /app
RUN chown django /app

USER django

WORKDIR /app

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["bash", "-c", "/start"]