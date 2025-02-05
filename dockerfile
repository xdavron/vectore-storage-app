# Use an official lightweight Python image.
FROM python:3.12-slim

# Install ffmpeg and clean up to reduce image size
RUN apt-get update && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .


