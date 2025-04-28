# Use an official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install Python dependencies without caching
RUN pip install --no-cache-dir -r requirements.txt

# Update package lists and install Chromium and its driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

# Copy the application code into the container
COPY app ./app

# Start the Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
