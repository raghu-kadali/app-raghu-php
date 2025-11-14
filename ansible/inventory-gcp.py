#!/usr/bin/env python3
import subprocess
import json
import sys

def get_mig_instances():
    try:
        # Get external IPs for direct SSH
        cmd = [
            "gcloud", "compute", "instances", "list",
            "--filter=name:php-instance-*", 
            "--format=value(EXTERNAL_IP)"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        inventory = {
            "php_servers": {
                "hosts": [],
                "vars": {
                    "ansible_user": "root",
                    "ansible_ssh_pass": "password123",
                    "ansible_become": "yes",
                    "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
                }
            }
        }
        
        ips = result.stdout.strip().split('\n')
        for ip in ips:
            if ip.strip():
                inventory["php_servers"]["hosts"].append(ip.strip())
        
        return inventory
        
    except Exception as e:
        return {"php_servers": {"hosts": []}}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(get_mig_instances()))
    else:
        print(json.dumps({}))
