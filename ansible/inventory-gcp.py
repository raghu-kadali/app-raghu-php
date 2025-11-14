#!/usr/bin/env python3
import subprocess
import json
import sys

def get_mig_instances():
    try:
        # Get instances from the php-mig managed instance group
        cmd = [
            "gcloud", "compute", "instance-groups", "list-instances", 
            "php-mig", "--region=us-central1", "--format=json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"Error getting MIG instances: {result.stderr}", file=sys.stderr)
            return {"php_servers": {"hosts": []}}
        
        instances = json.loads(result.stdout)
        
        inventory = {
            "php_servers": {
                "hosts": [],
                "vars": {
                    "ansible_user": "ubuntu",
                    "ansible_become": "yes",
                    "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
                }
            }
        }
        
        # Get external IPs for each instance in the MIG
        for instance in instances:
            instance_name = instance["instance"].split("/")[-1]
            
            # Get the external IP for this specific instance
            ip_cmd = [
                "gcloud", "compute", "instances", "describe", instance_name,
                "--zone=us-central1-f", 
                "--format=value(networkInterfaces[0].accessConfigs[0].natIP)"
            ]
            ip_result = subprocess.run(ip_cmd, capture_output=True, text=True, timeout=10)
            
            if ip_result.returncode == 0 and ip_result.stdout.strip():
                external_ip = ip_result.stdout.strip()
                inventory["php_servers"]["hosts"].append(external_ip)
                print(f"Added instance {instance_name} with IP {external_ip}", file=sys.stderr)
        
        print(f"Found {len(inventory['php_servers']['hosts'])} instances in php-mig", file=sys.stderr)
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
