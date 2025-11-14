#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import time

def setup_ssh_keys():
    """Automatically set up SSH keys for all PHP instances"""
    try:
        # Generate SSH key if not exists
        ssh_key_path = os.path.expanduser("~/.ssh/ansible_key")
        if not os.path.exists(ssh_key_path):
            os.makedirs(os.path.dirname(ssh_key_path), exist_ok=True)
            subprocess.run([
                "ssh-keygen", "-t", "rsa", "-N", "", "-f", ssh_key_path
            ], capture_output=True, check=True)
            print("Generated SSH key", file=sys.stderr)
        
        # Read public key
        with open(ssh_key_path + ".pub", "r") as f:
            pub_key = f.read().strip()
        
        # Get all PHP instances
        instances_cmd = [
            "gcloud", "compute", "instances", "list",
            "--filter=name:php-instance-*", 
            "--format=json"
        ]
        instances_result = subprocess.run(instances_cmd, capture_output=True, text=True, timeout=30)
        
        if instances_result.returncode == 0:
            instances = json.loads(instances_result.stdout)
            for instance in instances:
                instance_name = instance["name"]
                zone = instance["zone"].split("/")[-1]
                
                # Remove any existing ubuntu SSH keys first
                subprocess.run([
                    "gcloud", "compute", "instances", "remove-metadata", instance_name,
                    f"--zone={zone}",
                    "--keys=ssh-keys",
                    "--quiet"
                ], capture_output=True, timeout=10)
                
                # Add SSH key to instance metadata
                subprocess.run([
                    "gcloud", "compute", "instances", "add-metadata", instance_name,
                    f"--zone={zone}",
                    f"--metadata=ssh-keys=ubuntu:{pub_key}",
                    "--quiet"
                ], capture_output=True, timeout=10)
                print(f"Added SSH key to {instance_name}", file=sys.stderr)
                
                # Wait for metadata to apply
                time.sleep(10)
                
                # Test SSH connection
                test_ip = instance["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
                test_cmd = [
                    "ssh", "-i", ssh_key_path, "-o", "StrictHostKeyChecking=no",
                    "-o", "ConnectTimeout=10", f"ubuntu@{test_ip}", "echo 'SSH successful'"
                ]
                test_result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=15)
                if test_result.returncode == 0:
                    print(f"SSH test successful for {test_ip}", file=sys.stderr)
                else:
                    print(f"SSH test failed for {test_ip}: {test_result.stderr}", file=sys.stderr)
        
        return ssh_key_path
        
    except Exception as e:
        print(f"SSH setup error: {e}", file=sys.stderr)
        return None

def get_mig_instances():
    try:
        # First, set up SSH keys
        ssh_key_path = setup_ssh_keys()
        
        # Get instances from MIG with external IPs directly
        cmd = [
            "gcloud", "compute", "instances", "list",
            "--filter=name:php-instance-*", 
            "--format=value(EXTERNAL_IP)"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print(f"DEBUG: Found IPs: {result.stdout}", file=sys.stderr)
        
        inventory = {
            "php_servers": {
                "hosts": [],
                "vars": {
                    "ansible_user": "ubuntu",
                    "ansible_become": "yes",
                    "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=30",
                    "ansible_ssh_private_key_file": ssh_key_path if ssh_key_path else "~/.ssh/ansible_key"
                }
            }
        }
        
        # Add IPs directly
        ips = result.stdout.strip().split('\n')
        for ip in ips:
            if ip.strip():
                inventory["php_servers"]["hosts"].append(ip.strip())
                print(f"DEBUG: Added host: {ip.strip()}", file=sys.stderr)
        
        print(f"DEBUG: Final hosts: {inventory['php_servers']['hosts']}", file=sys.stderr)
        return inventory
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {"php_servers": {"hosts": []}}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(get_mig_instances()))
    elif len(sys.argv) == 2 and sys.argv[1] == "--host":
        print(json.dumps({}))
    else:
        print(json.dumps({}))
