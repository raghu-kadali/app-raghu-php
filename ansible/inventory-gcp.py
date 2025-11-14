#!/usr/bin/env python3
import subprocess
import json
import sys

def get_mig_instances():
    try:
        # Get just the external IPs in a simple way
        cmd = [
            "gcloud", "compute", "instances", "list",
            "--filter=name:php-instance-*", 
            "--format=value(EXTERNAL_IP)"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print(f"DEBUG: Command return code: {result.returncode}", file=sys.stderr)
        print(f"DEBUG: Command output: '{result.stdout}'", file=sys.stderr)
        
        inventory = {
            "php_servers": {
                "hosts": [],
                "vars": {
                    "ansible_user": "sa_107639644271753149281",
                    "ansible_become": "yes",
                    "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
                    "ansible_ssh_private_key_file": "~/.ssh/google_compute_engine"
                }
            }
        }
        
        # Split the output by lines and add each IP
        ips = result.stdout.strip().split('\n')
        for ip in ips:
            if ip.strip():  # Only add non-empty IPs
                inventory["php_servers"]["hosts"].append(ip.strip())
                print(f"DEBUG: Added IP: {ip.strip()}", file=sys.stderr)
        
        print(f"DEBUG: Final inventory has {len(inventory['php_servers']['hosts'])} hosts", file=sys.stderr)
        return inventory
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return {"php_servers": {"hosts": []}}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(get_mig_instances()))
    elif len(sys.argv) == 2 and sys.argv[1] == "--host":
        print(json.dumps({}))
    else:
        print(json.dumps({}))
