#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
# python manage.py createsuperuser --noinput
# python manage.py collectstatic --noinput

# users
python manage.py loaddata ./static/docs/db31012025.json

exec "$@"