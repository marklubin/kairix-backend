#!/bin/bash

# Ensure pyenv is initialized
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

# Initialize pyenv
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Activate virtualenv
pyenv activate kairix-env || { echo "Failed to activate pyenv virtualenv"; exit 1; }

# Parse command line arguments
SUITE=${1:-"all"}  # Default to "all" if no argument provided

case $SUITE in
    "unit")
        export FLASK_CONFIG=testing
        PYTHONPATH=. pytest --cov=app tests/models/ tests/services/ tests/routes/ -v
        ;;
    "e2e")
        export FLASK_CONFIG=devtest
        PYTHONPATH=. pytest --cov=app tests/e2e/ -v
        ;;
    "all")
        echo "Running all test suites..."
        
        echo "Running unit tests..."
        export FLASK_CONFIG=testing
        PYTHONPATH=. pytest --cov=app tests/models/ tests/services/ tests/routes/ -v
        
        echo "Running e2e tests..."
        export FLASK_CONFIG=devtest
        PYTHONPATH=. pytest --cov=app tests/e2e/ -v
        ;;
    *)
        echo "Invalid test suite specified. Available options: unit, e2e, all"
        exit 1
        ;;
esac

# Deactivate environment after tests
pyenv deactivate
