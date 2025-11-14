#!/usr/bin/env python3
import subprocess
import json
import sys

def get_mig_instances():
    try:
        # Get just the external IPs
        cmd = [
            "gcloud", "compute", "instances", "list",
            "--filter=name:php-instance-*", 
            "--format=value(EXTERNAL_IP)"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Get the service account email dynamically
        username = ""
        if result.stdout.strip():
            first_ip = result.stdout.strip().split('\n')[0]
            # Get instance name from IP
            instance_name_cmd = [
                "gcloud", "compute", "instances", "list",
                "--filter=EXTERNAL_IP=" + first_ip,
                "--format=value(NAME)"
            ]
            instance_name_result = subprocess.run(instance_name_cmd, capture_output=True, text=True, timeout=10)
            
            if instance_name_result.returncode == 0:
                instance_name = instance_name_result.stdout.strip()
                # Get zone for the instance
                zone_cmd = [
                    "gcloud", "compute", "instances", "list",
                    "--filter=EXTERNAL_IP=" + first_ip,
                    "--format=value(ZONE)"
                ]
                zone_result = subprocess.run(zone_cmd, capture_output=True, text=True, timeout=10)
                
                if zone_result.returncode == 0:
                    zone = zone_result.stdout.strip()
                    # Get service account from instance
                    sa_cmd = [
                        "gcloud", "compute", "instances", "describe", instance_name,
                        "--zone=" + zone, "--format=value(serviceAccounts.email)"
                    ]
                    sa_result = subprocess.run(sa_cmd, capture_output=True, text=True, timeout=10)
                    if sa_result.returncode == 0 and sa_result.stdout.strip():
                        username = sa_result.stdout.strip()
        
        # If we couldn't get the service account, fall back to OS Login username
        if not username:
            user_cmd = ["gcloud", "compute", "os-login", "describe-profile", "--format=value(posixAccounts.username)"]
            user_result = subprocess.run(user_cmd, capture_output=True, text=True, timeout=10)
            if user_result.returncode == 0:
                username = user_result.stdout.strip()
        
        inventory = {
            "php_servers": {
                "hosts": [],
                "vars": {
                    "ansible_user": username,
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
        
        print(f"DEBUG: Using username: {username}", file=sys.stderr)
        return inventory
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return {"php_servers": {"hosts": []}}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(get_mig_instances()))
    else:
        print(json.dumps({}))
