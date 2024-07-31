# Dockerfile for Flask Application
# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Dockerfile for Flask Application
# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disc and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]

