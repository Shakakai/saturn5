FROM nginx:1.19.3-alpine

RUN apk update && apk upgrade && apk add wget && apk add bash

RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash

# Create user and group
RUN addgroup --system web
RUN adduser --system --ingroup web web

# Setup Startup Script
COPY ./start-server.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown web /start

# Create directory to mount application files
RUN mkdir /app
RUN chown web /app

USER django

WORKDIR /app

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["bash", "-c", "/start"]