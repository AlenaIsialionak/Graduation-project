#!/bin/bash

echo "Apply database migrations"

python ./src/manage.py makemigrations
python ./src/manage.py migrate
python ./src/manage.py makemigrations news_app
python ./src/manage.py migrate