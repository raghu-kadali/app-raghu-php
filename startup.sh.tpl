# Delete the current file and create a new one with proper line endings
rm startup.sh.tpl

cat > startup.sh.tpl << 'EOF'
#!/bin/bash

# Log everything
exec > /var/log/startup.log 2>&1

echo "=== Starting instance configuration ==="

# Install dependencies
apt-get update
apt-get install -y python3-pip curl gnupg

# Install gcloud SDK for gsutil and Artifact Registry auth
echo "Installing Google Cloud SDK..."
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list
apt-get update && apt-get install -y google-cloud-sdk

# Install Ansible
echo "Installing Ansible..."
pip3 install ansible

# Authenticate with Artifact Registry to pull the image
echo "Authenticating with Artifact Registry..."
gcloud auth configure-docker us-central1-docker.pkg.dev

# Get playbook from GCS
echo "Downloading Ansible playbook from GCS..."
gsutil cp gs://{{gcs_ansible_bucket}}/site.yml /tmp/site.yml

# Run playbook on THIS machine
echo "Running Ansible playbook..."
ansible-playbook -c local -i localhost, /tmp/site.yml --extra-vars "image_uri={{image_uri}} project={{project}}"

echo "=== Instance configuration complete ==="
EOF