#!bin/bash

# Exits after first failure
set -e

echo "Waiting for PostgreSQL..."

while ! pg_isready -h $DB_HOST -p ${DB_PORT:-5432} -U $DB_USER; do
    sleep 1
done    

echo "PostgreSQL is ready!"


case "$1" in
    migrate)
        echo "Running migrations..."
        python manage.py migrate
        ;;
    
    makemigrations)
        echo "Creating migrations..."
        python manage.py makemigrations
        ;;

    *)
        # If no matching found then all arguments are passed
        exec "$@"
        ;;
# closes the case
esac