#!/bin/bash

E_NO_POSTGRES_USERNAME=60

POSTGRES_USERNAME="$1"
DATABASE_NAME="Channel_Subscriber"

# Check if a username is provided
if [[ -z "$POSTGRES_USERNAME" ]]; then
  echo "Call $(basename $0) with your PostgreSQL user as the first argument."
  exit "$E_NO_POSTGRES_USERNAME"
fi

# Drop the database if it exists
dropdb --if-exists --username="$POSTGRES_USERNAME" "$DATABASE_NAME"

# Create a new database with the given owner
createdb --username="$POSTGRES_USERNAME" --owner="$POSTGRES_USERNAME" "$DATABASE_NAME"

# Run Django migrations
python manage.py migrate
