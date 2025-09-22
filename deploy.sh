#!/bin/bash
git pull origin main
docker-compose down
docker-compose up -d --build
docker-compose exec web_lms python manage.py migrate --noinput
#docker-compose exec web_lms python manage.py collectstatic --noinput
