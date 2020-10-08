FROM shakakai/python-base:latest

# Create user and group
RUN addgroup --system django
RUN adduser --system --ingroup django django

# Setup Startup Script
COPY ./start-server.sh /start
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