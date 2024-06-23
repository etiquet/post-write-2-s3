# IMPORTANT : THIS CODE DOES NOT RUN "YET" INTO OPENSHIFT ( error on temp folder recognition )

# Use an official Python runtime as a parent image
FROM python:3.8-slim as builder

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app

# Install the dependencies
RUN pip install --no-cache-dir flask boto3 gunicorn

# Use a distroless Python image as a base
FROM gcr.io/distroless/python3:nonroot

# Set the working directory
WORKDIR /app

# Copy the dependencies and the app from the builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.8/site-packages /app/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

ENV PYTHONPATH /app/site-packages

# Command to run the application
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app"]
