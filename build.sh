#!/bin/sh

echo "Building the application..."
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8001
