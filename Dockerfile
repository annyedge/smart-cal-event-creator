# Start from the Ollama image so Ollama is fully configured
FROM ollama/ollama:latest

# Set the working directory
WORKDIR /app

# Install Python 3.11, pip, Poetry, and other system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    curl \
    git \
    wget \
    gnupg \
    ca-certificates \
    bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir poetry

# Set environment variables for Ollama
ENV OLLAMA_LLM_LIBRARY=/usr/bin/
ENV OLLAMA_MODELS=/root/.ollama/models/

# Create directories for Ollama models
RUN mkdir -p /root/.ollama/models && chmod 700 /root/.ollama /root/.ollama/models

# Copy project configuration and install Python dependencies with Poetry
COPY .python-version pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY . /app/

# Expose the necessary ports
EXPOSE 8000
EXPOSE 11434

# Set a health check for the FastAPI service
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD curl -f http://localhost:8000/health || exit 1

# Clear the ENTRYPOINT set by the base image
ENTRYPOINT []

# Use bash to run multiple commands:
# 1. Start Ollama in the background and log output
# 2. Wait 5 seconds for it to be ready
# 3. Pull the desired model
# 4. Start FastAPI via uvicorn
CMD ["/bin/bash", "-c", "ollama serve > /app/ollama.log 2>&1 & sleep 5 && ollama pull llama2:7b && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
