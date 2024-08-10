# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Set working directory
WORKDIR /app

# Copy the Flask application and static files
COPY server.py /app/
COPY index.html /app/
COPY script.js /app/
COPY styles.css /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for the Flask app
EXPOSE 8080

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
