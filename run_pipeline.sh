#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Create the data directory if it doesn't exist
echo "Creating data directory if it doesn't exist..."
mkdir -p data

# Step 2: Build the Docker image
echo "Building Docker image..."
docker build -t fake-ingestion .

# Step 3: Run the Docker container and mount the data directory
echo "Running the Docker container..."
docker run --rm -v $(pwd)/data:/app/data fake-ingestion

# Step 4: Output completion message
echo "Pipeline completed successfully!"
