#!/bin/bash
set -e

# Wait for database to be ready
DB_HOST=${DB_HOST:-db}
echo "Waiting for database at $DB_HOST:5432..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn
echo "Starting gunicorn..."
exec gunicorn CountyNavigator.wsgi:application --bind 0.0.0.0:${PORT:-8000}
