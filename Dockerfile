# BUILD STAGE
FROM python:3.12-slim-bullseye AS builder

# Disable writing of .pyc files and enable unbuffered stdout/stderr for better logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Enable pre-compiling Python bytecode for faster app startup
ENV UV_COMPILE_BYTECODE=1

# Copy all installed packages into the environment to ensure full isolation
ENV UV_LINK_MODE=copy

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat \
        gcc \
        wget \
        curl \
        unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set work directory and copy necessary files
WORKDIR /opt
COPY pyproject.toml uv.lock  ./
COPY ./backend ./backend

# Install project dependencies
RUN uv sync --frozen --no-cache

# RUN STAGE
# Use another Python 3.12 slim image for the runtime environment, keeping the final image minimal
FROM python:3.12-slim-bullseye

# Copy the entire application (code and dependencies) from the builder stage
COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /opt /opt/

WORKDIR /opt

# Expose the application port
EXPOSE 8000

# Command to run the application
# CMD ["uv", "run", "backend/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["backend/manage.py", "runserver", "0.0.0.0:8000"]