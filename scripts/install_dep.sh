#!/bin/bash

# Usage: ./install_dep.sh package_name

# Check if a package name was provided
if [ -z "$1" ]; then
  echo "Usage: $0 package_name"
  exit 1
fi

PACKAGE_NAME=$1

# Detect and activate virtual environment
if [ -d "venv" ]; then
  source venv/bin/activate  # Mac/Linux
elif [ -d "venv/Scripts" ]; then
  source venv/Scripts/activate  # Windows
else
  echo "Error: Virtual environment not found. Please create one first."
  exit 1
fi

# Check if the correct venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "Error: Failed to activate virtual environment."
  exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Install the package inside the venv
pip install "$PACKAGE_NAME"

# Update requirements.txt
pip freeze | grep "^$PACKAGE_NAME==" >> requirements.txt

echo "✅ Installed $PACKAGE_NAME and updated requirements.txt"

# Deactivate venv after installation (optional)
deactivate

echo "✅ Virtual environment deactivated"