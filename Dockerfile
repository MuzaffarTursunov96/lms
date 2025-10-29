FROM python:3.11.3-slim

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (important for production)
# RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Gunicorn as WSGI server
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
