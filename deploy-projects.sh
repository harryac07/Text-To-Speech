#!/bin/bash

# Function to deploy a project
deploy_project() {
    project_dir="$1"
    local_port="$2"

    # Build Docker image
    (cd "$project_dir" && docker build --no-cache -t "${project_dir}:latest" .)

    # Apply Deployment and Service YAML files
    kubectl apply -f "${project_dir}/deployment.yaml"
    kubectl apply -f "${project_dir}/service.yaml"

    # Port forward in the background with the specified local port
    nohup kubectl port-forward service/"${project_dir}-service" "${local_port}":80 &
}

# Configure your Docker client to interact with the Docker daemon inside your Minikube
eval $(minikube docker-env)

# Deploy the "frontend" project with local port 3000
deploy_project "frontend" 3000

# Deploy the "text-to-speech" project with local port 3001
deploy_project "text-to-speech" 3001

# Deploy the "translate-api" project with local port 3002
deploy_project "translate-api" 3002

# Sleep to allow time for port forwarding
sleep 5

# List the running port-forwarding processes
ps aux | grep 'kubectl port-forward'

echo "All services deployed and port-forwarding started."
