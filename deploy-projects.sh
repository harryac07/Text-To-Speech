#!/bin/bash

# Function to check if a port is available and kill any conflicting processes
check_and_kill_port() {
    local port="$1"
    if lsof -i :$port; then
        echo "Port $port is already in use. Attempting to kill the conflicting process..."
        kill $(lsof -t -i :$port)
        sleep 2  # Wait for the process to terminate
        if lsof -i :$port; then
            echo "Failed to kill the conflicting process using port $port. Please resolve the conflict manually."
            exit 1
        else
            echo "Conflicting process using port $port has been terminated."
        fi
    fi
}

# Function to deploy a project and establish port-forwarding with a timeout
deploy_project() {
    project_dir="$1"
    local_port="$2"
    timeout_seconds=60  # Set the timeout duration for port-forwarding (60 seconds)
    start_time=$(date +%s)  # Record the start time
    
    # Check and kill any conflicting process using the local port
    check_and_kill_port $local_port

    # Build Docker image
    (cd "$project_dir" && docker build --no-cache -t "${project_dir}:latest" .)

    # Apply Deployment and Service YAML files
    kubectl apply -f "${project_dir}/deployment.yaml"
    kubectl apply -f "${project_dir}/service.yaml"

    # Start port-forwarding in the background, mapping local_port to container_port
    (nohup kubectl port-forward service/"${project_dir}-service" "${local_port}":80 &)

    # Record the background process ID (PID)
    local pid=$!

    while true; do
        # Check if the port-forwarding process is still running
        if ! ps -p $pid > /dev/null; then
            echo "Port-forwarding for $project_dir succeeded."
            break  # Port-forwarding is successful; exit the loop
        fi

        # Get the current time and check if the timeout has been reached
        current_time=$(date +%s)
        if ((current_time - start_time >= timeout_seconds)); then
            echo "Port-forwarding process for $project_dir timed out after $timeout_seconds seconds. Killing the process."
            kill $pid  # Terminate the background process
            return 1  # Return an error code to indicate the port-forwarding timeout
        fi

        # Sleep for a short interval before checking again
        sleep 2
    done
}

# Configure your Docker client to interact with the Docker daemon inside your Minikube
eval $(minikube docker-env)

# Deploy the "image-to-number-api" project with local port 3001
deploy_project "image-to-number-api" 3001

# Deploy the "word-to-speech-api" project with local port 3002
deploy_project "word-to-speech-api" 3002

# Deploy the "number-to-word-api" project with local port 3003
deploy_project "number-to-word-api" 3003

# Deploy the "backend-api" project with local port 3004
deploy_project "backend-api" 3004

# Deploy the "frontend" project with local port 3000
deploy_project "frontend" 3000

echo "All services deployed and port-forwarding started."
