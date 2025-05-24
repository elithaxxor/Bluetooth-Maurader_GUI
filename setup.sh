#!/bin/bash
set -e

# Create and activate the virtual environment
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "ERROR: requirements.txt not found!"
  exit 1
fi

# Find the main file and run it
if [ -f "main.py" ]; then
  python main.py
elif [ -f "final_bluetooth_app_codebase 2/main.py" ]; then
  python "final_bluetooth_app_codebase 2/main.py"
else
  echo "ERROR: Could not find main.py entry point!"
  exit 1
fi
