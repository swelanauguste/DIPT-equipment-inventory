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
python manage.py createsuperuser --noinput
# python manage.py collectstatic --noinput

# users
python manage.py loaddata ./static/docs/users/department_list.json
python manage.py loaddata ./static/docs/users/location_list.json
python manage.py add_user_list
python manage.py update_technical_roles

# computers
python manage.py loaddata ./static/docs/computers/status_list.json
python manage.py loaddata ./static/docs/computers/operating_system_list.json
python manage.py loaddata ./static/docs/computers/maker_list.json
python manage.py loaddata ./static/docs/computers/monitor_model_list.json
python manage.py loaddata ./static/docs/computers/monitor_list.json
python manage.py get_monitor_and_models_slug

python manage.py loaddata ./static/docs/computers/computer_model_list.json
python manage.py update_computer_type
python manage.py add_computer_list
python manage.py loaddata ./static/docs/computers/microsoft_version_list.json
python manage.py loaddata ./static/docs/computers/microsoft_list.json

# printers
python manage.py loaddata ./static/docs/printers/printer_model_list.json
python manage.py loaddata ./static/docs/printers/printer_list.json
python manage.py get_printer_and_models_slug

# tickets
python manage.py loaddata ./static/docs/tickets/ticket_status_list.json
python manage.py loaddata ./static/docs/tickets/ticket_category_list.json
python manage.py add_ticket_list
python manage.py loaddata ./static/docs/tickets/ticket_comment_list.json

exec "$@"