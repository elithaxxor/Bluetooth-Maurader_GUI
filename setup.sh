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

echo "Which version do you want to run?"
echo "1) GUI (PyQt6)"
echo "2) CLI"
read -p "Enter 1 or 2 [1]: " choice

# Default to GUI if no input
choice="${choice:-1}"

if [ "$choice" = "1" ]; then
  # Try both possible locations for main.py
  if [ -f "main.py" ]; then
    python main.py
  elif [ -f "final_bluetooth_app_codebase 2/main.py" ]; then
    python "final_bluetooth_app_codebase 2/main.py"
  else
    echo "ERROR: Could not find GUI main.py entry point!"
    exit 1
  fi
elif [ "$choice" = "2" ]; then
  # Try both possible locations for CLI main_II.py
  if [ -f "main_II.py" ]; then
    python main_II.py
  elif [ -f "final_bluetooth_app_codebase 2/main_II.py" ]; then
    python "final_bluetooth_app_codebase 2/main_II.py"
  else
    echo "ERROR: Could not find CLI main_II.py entry point!"
    exit 1
  fi
else
  echo "Invalid choice."
  exit 1
fi
