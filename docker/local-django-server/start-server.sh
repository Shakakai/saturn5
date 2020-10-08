#!/bin/bash

#set -o errexit
#set -euxo pipefail
#set -o nounset

cd /app || exit

echo "Install python dependencies"
pipenv install

echo "Collect static files for django"
pipenv run python manage.py collectstatic --clear --noinput # clearstatic files
pipenv run python manage.py collectstatic --noinput  # collect static files

echo "Run migrations"
pipenv run python manage.py migrate

echo "Starting dev server..."
pipenv run python manage.py runserver "$DJANGO_PORT"
