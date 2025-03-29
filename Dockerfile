# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir psycopg[binary]
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Django app will run on
EXPOSE 8000

# Define the command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
