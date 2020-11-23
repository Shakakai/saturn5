#!/bin/bash

#set -o errexit
#set -euxo pipefail
#set -o nounset

cd /app || exit

eval "$FRONTEND_BUILD_CMD"

if [ -z "$FRONTEND_BUILD_DIR" ]
then
  echo "\$FRONTEND_BUILD_DIR doesn't exist"
  exit 1
fi

echo "Frontend Build Directory: $FRONTEND_BUILD_DIR"

if [ -z "$FRONTEND_DEV_CMD" ]
then
  echo "\$FRONTEND_DEV_CMD doesn't exist"
  exit 1
else
  eval "$FRONTEND_DEV_CMD"
fi
