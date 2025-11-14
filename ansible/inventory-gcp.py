#!/usr/bin/env python3
import subprocess
import json
import sys
import os

def get_mig_instances():
    try:
        # Get just the external IPs
        cmd = [
            "gcloud", "compute", "instances", "list",
            "--filter=name:php-instance-*", 
            "--format=value(EXTERNAL_IP)"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Get the current OS Login username from the Ansible master
        user_cmd = ["gcloud", "compute", "os-login", "describe-profile", "--format=value(posixAccounts.username)"]
        user_result = subprocess.run(user_cmd, capture_output=True, text=True, timeout=10)
        username = user_result.stdout.strip()
        
        inventory = {
            "php_servers": {
                "hosts": [],
                "vars": {
                    "ansible_user": username,  # Use the OS Login username
                    "ansible_become": "yes",
                    "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
                }
            }
        }
        
        # Split the output by lines and add each IP
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
