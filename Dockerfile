# Use a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV DB_PATH=/app/db/fitness_tracker.db

# Create database directory
RUN mkdir -p /app/db

# Run the database initialization script
RUN bash create_db.sh

# Expose the application port
EXPOSE 5000

# Command to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
