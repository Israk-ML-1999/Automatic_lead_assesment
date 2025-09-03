FROM python:3.11-slim

WORKDIR /app

# Install system deps for WeasyPrint (Debian 12+ package names)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    libfreetype6 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure folders
RUN mkdir -p data reports

# Create demo leads if missing
RUN python scripts/make_sample_leads.py || true

EXPOSE 8000
