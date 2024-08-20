# proj/Dockerfile

# Base image
FROM python:3.11.4-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Install dependencies
COPY proj/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Add wait-for-it script
COPY proj/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Create a non-root user
RUN useradd -m yonza
USER yonza

# Run the application
CMD ["bash", "-c", "./wait-for-it.sh db:3306 -s -t 60 -- python manage.py migrate && gunicorn --bind 0.0.0.0:8000 proj.wsgi:application"]
