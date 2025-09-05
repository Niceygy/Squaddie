#!/bin/bash

clear

# Pip

rm requirements.txt && pip freeze >> requirements.txt

# Build the Docker image
docker build -t niceygy/squaddie .

# Tag the Docker image
docker tag niceygy/squaddie ghcr.io/niceygy/squaddie:latest

# Push the Docker image to GH registry
docker push ghcr.io/niceygy/squaddie:latest

#Update local container

cd /opt/stacks/elite_apps

docker compose pull

docker compose down

docker compose up -d

docker logs squaddie -f
