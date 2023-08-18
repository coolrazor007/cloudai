# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Declare the build argument
ARG HUGGINGFACE_API_KEY

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HUGGINGFACE_API_KEY $HUGGINGFACE_API_KEY

# Set work directory
WORKDIR /app

RUN apt-get update && apt-get install -y git 

#git config --global credential.store

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app/

#RUN huggingface-cli login --token $HUGGINGFACE_API_KEY

# Run the command to start Uvicorn
#CMD ["huggingface-cli", "login", "--token", "${HUGGINGFACE_API_KEY}", "&&", "uvicorn", "main:app", "--host", "0.0.0.0"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

CMD huggingface-cli login --token $HUGGINGFACE_API_KEY && uvicorn main:app --host 0.0.0.0
