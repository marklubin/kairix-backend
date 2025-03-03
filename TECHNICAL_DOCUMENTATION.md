# Technical Documentation for Kairix Backend

## Overview
The Kairix backend serves as a conversational AI service, integrating OpenAI's models with retrieval-augmented generation (RAG) and fine-tuning capabilities. It is designed for easy deployment on AWS and provides a flexible chat AI service that retains conversation context and can call external functions.

## Codebase Structure
### Root Files
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **.python-version**: Specifies the Python version for the project.
- **README.md**: Documentation for the project.
- **requirements.txt**: Lists the dependencies required for the project.
- **run.py**: Entry point for running the application.
- **system-install.sh**: Script for system installation.
- **TODO.md**: List of tasks to be completed.

### Application Directory (`app/`)
- **`__init__.py`**: Initializes the application package.
- **`config.py`**: Configuration settings for the application.
- **`models.py`**: Defines the data models used in the application.
- **Routes Directory (`routes/`)**:
  - **`agents.py`**: Routes related to agents.
  - **`conversations.py`**: Routes related to conversations.
  - **`messages.py`**: Routes related to messages.
  - **`users.py`**: Routes related to users.
- **Services Directory (`services/`)**:
  - **`memory_provider.py`**: Service for managing memory.
  - **`openai_service.py`**: Service for interacting with OpenAI.

### Migrations Directory (`migrations/`)
- **`alembic.ini`**: Configuration file for Alembic migrations.
- **`env.py`**: Environment setup for migrations.
- **`README`**: Documentation for migrations.
- **`script.py.mako`**: Template for migration scripts.

### Scripts Directory (`scripts/`)
- **`install_dep.sh`**: Script for installing dependencies.
- **`run_local.sh`**: Script for running the application locally.
- **`run_tests.sh`**: Script for running tests.

### Tests Directory (`tests/`)
- **`conftest.py`**: Configuration for pytest.
- **E2E Tests Directory (`e2e/`)**: Contains end-to-end tests for various flows.
- **Models Tests Directory (`models/`)**: Tests for models.
- **Routes Tests Directory (`routes/`)**: Tests for routes.
- **Services Tests Directory (`services/`)**: Tests for services.

## Requirements Folder
The `requirements` folder contains the original PDF documents that provide detailed information about the Kairix system, including domain models, technical guides, and high-level overviews.

## Changelog
- **3/2/25**: Initial creation of the technical documentation.
- **3/2/25**: Added a Git pre-commit hook to ensure all tests pass and coverage is above 80% before committing changes.
- **3/2/25**: Added a `requirements` folder containing original PDF documents related to the Kairix system.
