#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
# python manage.py collectstatic --clear --noinput
if [[ $? -eq 0 ]]
then
    echo "Starting app..."
    sleep 2
    python manage.py runserver 0.0.0.0:8000
else
  python manage.py runserver 0.0.0.0:8000
fi

exec "$@"