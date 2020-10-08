#!/bin/bash

#set -o errexit
#set -euxo pipefail
#set -o nounset

cd /app || exit
cd "$BACKEND_PATH" || exit

echo "Starting celery worker & scheduler processes..."
celery -A proj worker -l info
