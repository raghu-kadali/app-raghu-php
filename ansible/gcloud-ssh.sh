#!/bin/bash
# gcloud-ssh.sh - SSH wrapper that uses gcloud compute ssh

# Extract IP from arguments
IP="$1"
shift

# Get instance name and zone from IP
INSTANCE_INFO=$(gcloud compute instances list --filter="networkInterfaces[0].accessConfigs[0].natIP=$IP" --format="value(NAME,ZONE)")
INSTANCE_NAME=$(echo "$INSTANCE_INFO" | cut -d' ' -f1)
ZONE=$(echo "$INSTANCE_INFO" | cut -d' ' -f2)

# Use gcloud compute ssh with all remaining arguments
exec gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --ssh-flag="$@"
