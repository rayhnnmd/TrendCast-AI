# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy to allow PDF/Text operations
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create output directories
RUN mkdir -p output/videos output/audio output/backgrounds output/scheduler output/temp credentials

# Set environment variables (Override these in your deployment platform)
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose port 5000
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
