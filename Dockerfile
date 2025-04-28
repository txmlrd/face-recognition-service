# Gunakan image Python
FROM python:3.10-slim

# Install library OS-level untuk DeepFace
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx

RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# HANYA copy requirements.txt dulu
COPY requirements.txt .

# Install dependency Python
RUN pip install --no-cache-dir -r requirements.txt

# Baru copy semua source code
COPY . .

# Default command
CMD ["python","app/run.py"]
