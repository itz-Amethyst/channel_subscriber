# 🐍 Django Project with Docker and Celery Beat 🥦

## Overview
This project built upon Django with Docker for local development and Celery Beat for periodic task scheduling. Follow this instructions for setting up the project, building Docker images, running Django, and configuring Celery Beat.


### 1. Install Dependencies
Ensure all required Python packages are installed.

```bash
pip install -r requirements.txt
```
### 2. Docker Setup
To build the Docker image:

```bash
docker build -t my-django-app .
```
To run the Docker container:

```bash
docker run -p 8000:8000 my-django-app
```

### 3. Running the Django Project
After running the Docker container, you can open the Django project at:
```
http://localhost:8000
```

### 4. Setting up Celery Beat
To set up Celery Beat with periodic tasks, run the following command:

```bash
python manage.py <your_celery_beat_command>
```

Running Django Commands in Docker
To run Django management commands within the Docker container:

```
bash
docker exec -it <container-name> python manage.py <command>
```

Replace <container-name> with the name or ID of your running container, and <command> with the Django command you want to run.

## Running locally

### 1. Install Dependencies
Ensure all required Python packages are installed. Run the following command in your terminal:
```bash
pip install -r requirements.txt
```

### 2. Apply migrations

```bash
python manage.py makemigrations
```

and then

```bash
python manage.py migrate
```

### 3. Final step
Now with having these steps done you can easily access the project on your local

```bash
python manage.py runserver
```
