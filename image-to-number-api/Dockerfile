# Use a slim version of the official Python runtime
FROM python:3.9-slim

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Update pip and install your Python dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

# Expose port 3001 for your FastAPI application
EXPOSE 3001

# Copy your application code into the container
COPY . /code

# Command to run your FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
