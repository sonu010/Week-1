# Use a multi-stage build with a Python 3.8 image as the builder stage
FROM python:3.8 AS builder

WORKDIR /app

COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use a minimal base image for the final stage
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the wait-for-it script before starting the application
CMD ["./wait-for-it.sh", "db:3306", "--", "python", "app.py"]
