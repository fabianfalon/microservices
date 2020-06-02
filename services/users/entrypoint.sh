#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z places-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python main.py db init
python main.py db migrate
python main.py db upgrade

python main.py runserver -h 0.0.0.0