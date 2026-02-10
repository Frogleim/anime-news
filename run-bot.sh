#!/bin/bash

# Stop and remove existing container if it exists
docker stop news_bot || true
docker rm news_bot || true

# Build the Docker image
docker build -t news_bot .

# Run the container with restart policy and volume mount for persistent storage
docker run -d \
    --name news_bot \
    --restart always \
    -v "$(pwd)/.env:/app/.env:ro" \
    -v "$(pwd)/data:/app/data" \
    news_bot

# Show logs
docker logs -f news_bot