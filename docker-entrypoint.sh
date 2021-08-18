#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python src/manage.py migrate

# Create a superuser if it does not exist
echo "Creating default super user from environment variables"
python src/manage.py createsuperuser --noinput

# Start server
echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000