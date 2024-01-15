#!/bin/bash
# Purpose: Run streamlit application, ensuring that the `src` sub-modules are in the path
# (This emulates PyCharm's run configuration button parameter: `add content roots to PYTHONPATH`)

# Find the absolute path to the project root
PROJECT_ROOT=$(realpath "$(dirname "$0")/..")

# Set PYTHONPATH to the project root, ensuring it's not added multiple times
export PYTHONPATH=$(echo $PYTHONPATH | tr ":" "\n" | grep -v "$PROJECT_ROOT" | tr "\n" ":")$PROJECT_ROOT

venv/bin/streamlit run src/streamlit_app/app.py
