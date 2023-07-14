# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

ENV POSTGRES_PASSWORD=456
# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "load_data.py"]
