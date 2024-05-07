# # Stage 1: Build Stage
# FROM python:3.11-slim AS builder

# # Set the working directory to /app
# WORKDIR /app

# # Copy only the requirements file to install dependencies
# COPY requirements.txt .

# # Install any needed packages specified in requirements.txt
# RUN apt-get update \
#     && python -m venv /app/venv \
#     && /app/venv/bin/pip install --no-cache-dir -r requirements.txt \
#     && rm -rf /root/.cache

# # Stage 2: Runtime Stage
# FROM python:3.11-slim 

# # Set the working directory to /app
# WORKDIR /app

# # Copy the virtual environment from the build stage
# COPY --from=builder /app/venv /app/venv

# # Copy application code
# COPY . .

# # Install dependencies from requirements.txt
# RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt \
#     && rm -rf /root/.cache

# # Make port 5066 available to the world outside this container
# EXPOSE 5066

# # Define environment variable

# CMD ["/app/venv/bin/python", "app.py"]

FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Expose the port Gunicorn will listen on
EXPOSE 5066

# Command to run the application using Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5066"]
