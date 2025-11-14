#!/bin/bash

# Install Docker
apt update -y
apt install docker.io -y
systemctl enable docker
systemctl start docker

# Authenticate Docker with Artifact Registry (uses instance service account)
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# Pull and run PHP application container
docker pull us-central1-docker.pkg.dev/siva-477505/php-app/php-app:v1
docker run -d --name php-app -p 80:80 --restart unless-stopped us-central1-docker.pkg.dev/siva-477505/php-app/php-app:v1

echo "PHP application deployed successfully"
