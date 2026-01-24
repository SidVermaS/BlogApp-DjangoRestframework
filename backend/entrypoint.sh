#!/bin/sh

# Exits after first failure
set -e

echo "Waiting for PostgreSQL..."

while ! pg_isready -h $POSTGRES_HOST -p ${POSTGRES_PORT} -U $POSTGRES_USER; do
    sleep 1
done 

echo "PostgreSQL is ready!"


case "$1" in
    both_migrate)
        echo "Creating migrations..."
        python manage.py makemigrations profiles
        python manage.py makemigrations
        echo "Running migrations..."
        python manage.py migrate profiles
        python manage.py migrate
        ;;

    makemigrations)
        echo "Creating migrations..."
        python manage.py makemigrations profiles
        python manage.py makemigrations
        ;;

    migrate)
        echo "Running migrations..."
        python manage.py migrate profiles
        python manage.py migrate
        ;;

    *)
        # If no matching found then all arguments are passed
        exec "$@"
        ;;
# closes the case
esac