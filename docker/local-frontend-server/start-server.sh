#!/bin/bash

#set -o errexit
#set -euxo pipefail
#set -o nounset

cd /app || exit

nvm install "$NODE_VERSION"
nvm use "$NODE_VERSION"
eval "$FRONTEND_BUILD_CMD"
# Link the build folder to the folder nginx serves content out of.
ln -s "$FRONTEND_BUILD_DIR" /usr/share/nginx/html

nginx-debug -g 'daemon off;' &

eval "$FRONTEND_DEV_CMD"
