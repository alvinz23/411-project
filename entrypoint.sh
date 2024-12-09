#!/bin/bash

# Load the environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Check if CREATE_DB is true, and run the database creation script if so
if [ "$CREATE_DB" = "true" ]; then
    echo "Initializing the database..."
    bash /app/create_db.sh
else
    echo "Skipping database initialization."
fi

# Start the Flask application
echo "Starting the Flask application..."
exec flask run --host=0.0.0.0 --port=5000
