# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the script is executable
RUN chmod +x edition-manager.py

# Run edition-manager.py when the container launches
CMD ["python", "edition-manager.py"]
