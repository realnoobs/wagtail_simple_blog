#!/usr/bin/env bash

python ./manage.py migrate
python ./manage.py createblogadmin
python ./manage.py collectstatic --noinput
python ./manage.py compress
