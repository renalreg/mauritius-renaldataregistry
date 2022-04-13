#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python src/manage.py migrate

# Load initial data
echo "Load initial data"
python src/manage.py loaddata src/renaldataregistry/fixtures/data.json

# Create a superuser if it does not exist
echo "Creating default super user from environment variables"
python src/manage.py createsuperuser --noinput

# Collect static files
python src/manage.py collectstatic --noinput

# Start server
echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000
