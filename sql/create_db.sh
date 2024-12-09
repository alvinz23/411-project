#!/bin/bash

# Set the default database path if not already set
DB_PATH=${DB_PATH:-/app/sql/fitness_tracker.db}

# Check if the database file already exists
if [ -f "$DB_PATH" ]; then
    echo "Recreating database at $DB_PATH."
    # Drop and recreate the tables
    sqlite3 "$DB_PATH" < /app/sql/create_fitness_tables.sql
    echo "Database recreated successfully."
else
    echo "Creating database at $DB_PATH."
    # Create the database for the first time
    sqlite3 "$DB_PATH" < /app/sql/create_fitness_tables.sql
    echo "Database created successfully."
fi
