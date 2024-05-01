# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.12-slim

# Fix python printing
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt  # Copy the requirements file
RUN pip install -r /app/requirements.txt  # Install dependencies

# Create the /app directory and set it as the working directory
RUN mkdir /app
WORKDIR /app

# Copy the Django project into the Docker container
COPY . /app/

# Set environment variables for Django
# Example: specify the Django settings module
ENV DJANGO_SETTINGS_MODULE=kernel.settings

# Run the Django development server on port 8000
# You can change the IP and port if needed
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]