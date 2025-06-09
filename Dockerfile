# Use the official lightweight Python image.
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Set environment variables from .env if needed (optional, but recommend setting via ECS Secrets)
# ENV DB_HOST=...
# ENV DB_USER=...
# ENV DB_PASSWORD=...
# ENV DB_NAME=...

# Run the Flask app
CMD ["python", "index.py"]
