# 1. Use an official Python runtime as a parent image
FROM python:3.10

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project files into the container
COPY . .

# 6. Expose port 8000
EXPOSE 8000

# 7. Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# 8. Run migrations and start Django server
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
