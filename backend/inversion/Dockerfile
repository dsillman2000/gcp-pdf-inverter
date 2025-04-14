# Poetry-based FastAPI app
FROM python:3.12-slim

# Set environment variables
ENV STORAGE_BACKEND=local

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libmagic1 \
    libgl1 \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*
# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
# Install Python dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root
# Copy the application code
COPY . .
# Expose the FastAPI port
EXPOSE 8000

# Volumes for local storage
RUN mkdir -p /app/storage
VOLUME /app/storage
RUN mkdir -p /app/storage/my-uuid
RUN cp /app/tests/data/test.pdf /app/storage/my-uuid/pre.pdf

# Start the FastAPI app with Uvicorn
ENTRYPOINT ["fastapi", "run", "inversion/main.py", "--port", "8000"]