#!/bin/bash

#set -o errexit
#set -euxo pipefail
#set -o nounset

cd /app || exit

echo "Starting celery worker & scheduler processes..."
celery -A proj worker -l info
