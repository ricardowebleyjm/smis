# Base image
FROM python:3.12-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with gunicorn
CMD ["gunicorn", "smis.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
