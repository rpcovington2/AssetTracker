FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for venv and building some Python packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3-venv \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy your application code
COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Activate venv and install dependencies
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 4500

# Use venv Python to run your app
CMD ["/app/venv/bin/python", "./main.py"]
