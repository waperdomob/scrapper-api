#!/bin/bash


python manage.py migrate --settings=settings

gunicorn --env DJANGO_DJANGO_SETTINGS_MODULE=settings swgi:application --bind 127.0.0.1:8000
python manage.py runserver 0.0.0.0:8000