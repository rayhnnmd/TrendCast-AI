# Use full Python 3.11 image (more stable for complex media libraries)
FROM python:3.11

# Install system dependencies + direct setuptools support
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    python3-setuptools \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy
RUN find /etc/ImageMagick* -name "policy.xml" -exec sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' {} +

# Set working directory
WORKDIR /app

# Ensure pip and setuptools are at the absolute latest versions first
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create output directories
RUN mkdir -p output/videos output/audio output/backgrounds output/scheduler output/temp credentials

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose port 5000
EXPOSE 5000

# Start the application using Gunicorn
# Using 1 worker because task state is stored in-memory
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "600", "app:app"]

