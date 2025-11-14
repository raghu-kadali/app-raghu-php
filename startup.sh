#!/bin/bash

# Install Docker
apt-get update -y
apt-get install -y docker.io
systemctl enable docker
systemctl start docker

# Install gcloud SDK
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list
apt-get install -y apt-transport-https ca-certificates gnupg curl
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
apt-get update && apt-get install -y google-cloud-sdk

# Authenticate Docker with Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# Pull and run PHP application container
docker pull us-central1-docker.pkg.dev/siva-477505/php-app/php-app:v1
docker run -d --name php-app -p 80:80 --restart unless-stopped us-central1-docker.pkg.dev/siva-477505/php-app/php-app:v1


echo "Startup script completed successfully"
