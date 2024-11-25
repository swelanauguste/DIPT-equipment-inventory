#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput

# users
python manage.py add_department_list
python manage.py add_location_list
python manage.py add_user_list

# computers
python manage.py add_status_list
python manage.py add_operating_system_list
python manage.py add_maker_list
python manage.py add_monitor_model_list
python manage.py add_monitor_list
python manage.py add_computer_model_list
python manage.py add_computer_list

# tickets
python manage.py add_ticket_status_list
python manage.py add_ticket_category_list
python manage.py add_ticket_list
python manage.py add_ticket_comment_list
