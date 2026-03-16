FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first for layer caching
COPY backend/pyproject.toml backend/poetry.lock* ./backend/

# Install dependencies (no dev deps, no virtualenv in container)
WORKDIR /app/backend
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev --no-root

# Copy the rest of the project
WORKDIR /app
COPY backend/ ./backend/
COPY investors/ ./investors/
COPY skills/ ./skills/
COPY prompts/ ./prompts/

WORKDIR /app/backend

EXPOSE 8000

CMD uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}
