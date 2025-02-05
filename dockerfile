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
## Copy the rest of the application code.
#COPY ./app ./app
#COPY ./.env ./.env
#
## Expose the port uvicorn will run on.
#EXPOSE 8000
#
## Run the application using uvicorn.
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

