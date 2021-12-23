#!/usr/bin/env bash
cd ./apps
python manage.py migrate
python manage.py createblogadmin
python manage.py collectstatic --noinput
