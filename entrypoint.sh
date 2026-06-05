#!/bin/sh
# entrypoint.sh

echo "Waiting for database..."
while ! nc -z database 5432; do
  sleep 0.5
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"