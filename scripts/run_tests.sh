#!/bin/bash

# Ensure pyenv is initialized
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

export FLASK_CONFIG=testing
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Activate virtualenv
pyenv activate kairix-env || { echo "Failed to activate pyenv virtualenv"; exit 1; }

export PYTHONPATH=$(pwd)
# Run tests
pytest

# Deactivate environment after tests
pyenv deactivate