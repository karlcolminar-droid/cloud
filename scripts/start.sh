#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py init_superuser
gunicorn recipe_project.wsgi --log-file -
