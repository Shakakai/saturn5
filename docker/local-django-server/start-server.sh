#!/bin/bash

#set -o errexit
#set -euxo pipefail
#set -o nounset

cd /app || exit

echo "Collect static files for django"
python manage.py collectstatic --clear --noinput # clearstatic files
python manage.py collectstatic --noinput  # collect static files

echo "Run migrations"
python manage.py migrate

echo "Starting dev server..."
python manage.py runserver "$DJANGO_PORT"
