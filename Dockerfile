# KeyAuth - Production Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for ML models
RUN mkdir -p backend/ml/models

# Expose port
EXPOSE 8000

# Default port for Railway (uses $PORT env var)
ENV PORT=8000

# Run the application - use shell form to expand $PORT
CMD uvicorn backend.main:app --host 0.0.0.0 --port $PORT
