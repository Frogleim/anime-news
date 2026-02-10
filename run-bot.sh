#!/bin/bash

# Add error handling
set -e

# Add logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

update_bot() {
    log "Updating bot from repository..."

    # Pull latest changes
    git pull

    # Check if there are any changes
    if git diff --name-only HEAD@{1} HEAD | grep -q '^'; then
        log "Changes detected, rebuilding container..."

        # Stop the existing container gracefully
        log "Stopping existing container..."
        docker stop news_bot || true

        # Remove the old container
        log "Removing old container..."
        docker rm news_bot || true

        # Remove the old image
        log "Removing old image..."
        docker rmi news_bot || true

        # Build new image
        log "Building new Docker image..."
        docker build -t news_bot .

        # Run new container
        log "Starting new container..."
        docker run -d \
            --name news_bot \
            --restart always \
            -v "$(pwd)/.env:/app/.env:ro" \
            -v "$(pwd)/data:/app/data" \
            news_bot

        log "Update completed successfully!"
    else
        log "No changes detected in code, skipping rebuild..."
    fi
}

# Check if we're updating
if [ "$1" = "update" ]; then
    update_bot
    log "Showing logs (Ctrl+C to exit)..."
    docker logs -f news_bot
    exit 0
fi

# Normal run procedure
if [ ! -f .env ]; then
    log "Error: .env file not found!"
    exit 1
fi

log "Stopping existing container..."
docker stop news_bot || true
docker rm news_bot || true

log "Building Docker image..."
docker build -t news_bot .

log "Starting container..."
docker run -d \
    --name news_bot \
    --restart always \
    -v "$(pwd)/.env:/app/.env:ro" \
    -v "$(pwd)/data:/app/data" \
    news_bot

log "Container started successfully!"
log "Showing logs (Ctrl+C to exit)..."
docker logs -f news_bot