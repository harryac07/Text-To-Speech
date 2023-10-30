# Use a slim version of the official Python runtime
FROM alpine:latest

RUN apk add --no-cache python3

RUN python -m ensurepip --upgrade

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Update pip and install your Python dependencies
RUN pip3 install --no-cache-dir -r /code/requirements.txt

# Expose port 3004 for your FastAPI application
EXPOSE 3004

# Copy your application code into the container
COPY . /code

# Command to run your FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3004"]
