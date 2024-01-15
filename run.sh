#!/bin/bash
# Purpose: Run local development environment including API server, PostgreSQL container, and Streamlit application

# Find the absolute path to the project root
PROJECT_ROOT=$(realpath "$(dirname "$0")/..")

# Set up the API server
uvicorn src.fastAPI_app.app:app --reload &

# Start a local PostgreSQL container
docker compose up -d

# Wait for a moment to ensure that the API server and PostgreSQL container are up
sleep 5

# Set PYTHONPATH to the project root, ensuring it's not added multiple times
export PYTHONPATH=$(echo $PYTHONPATH | tr ":" "\n" | grep -v "$PROJECT_ROOT" | tr "\n" ":")$PROJECT_ROOT

# Run the Streamlit application
venv/bin/streamlit run src/streamlit_app/app.py
