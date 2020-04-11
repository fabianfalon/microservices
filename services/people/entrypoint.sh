#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z people-db 5433; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

python manage.py run -h 0.0.0.0