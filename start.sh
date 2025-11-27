#!/bin/bash

# Function to extract host and port from DATABASE_URL
extract_db_info() {
    if [ -n "$DATABASE_URL" ]; then
        # Extract host and port from DATABASE_URL
        # Format: postgresql://user:password@host:port/database
        DB_HOST=$(echo $DATABASE_URL | sed -n 's|.*@\([^:]*\):\([^/]*\)/.*|\1|p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's|.*@\([^:]*\):\([^/]*\)/.*|\2|p')
    fi
}

# Wait for database to be ready
if [ -n "$DATABASE_URL" ]; then
    extract_db_info
    echo "Waiting for database at $DB_HOST:$DB_PORT..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
    echo "Database is ready!"
else
    echo "No DATABASE_URL set, skipping database wait"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start the application
echo "Starting application..."
exec "$@"
