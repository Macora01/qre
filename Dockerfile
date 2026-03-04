# Multi-stage Dockerfile for Coolify deployment
# Stage 1: Build React frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy frontend source
COPY frontend/ ./

# In production, use relative URLs (empty REACT_APP_BACKEND_URL = relative /api)
ENV REACT_APP_BACKEND_URL=""

# Build frontend for production
RUN yarn build

# Stage 2: Python backend with built frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including build tools
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Copy and install requirements
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt || \
    (echo "=== PIP INSTALL FAILED ===" && \
     echo "Trying with verbose output:" && \
     pip install -v -r /app/backend/requirements.txt)

# Copy backend code
COPY backend/ /app/backend/

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Create data directory for CSV files
RUN mkdir -p /app/data

# Expose port
EXPOSE 8001

# Environment variables
ENV PYTHONUNBUFFERED=1

# Start backend server
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8001"]



