#!/usr/bin/env python3
import subprocess
import json
import sys

def get_mig_instances():
    try:
        # Method 1: Try getting instances from the MIG
        cmd = [
            "gcloud", "compute", "instance-groups", "list-instances", 
            "php-mig", "--region=us-central1", "--format=json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print(f"DEBUG: MIG list command return code: {result.returncode}", file=sys.stderr)
        
        instances = []
        if result.returncode == 0:
            instances = json.loads(result.stdout)
            print(f"DEBUG: Found {len(instances)} instances in MIG", file=sys.stderr)
        else:
            print(f"DEBUG: MIG command failed, trying direct instances list", file=sys.stderr)
            # Method 2: Fallback to direct instances list
            cmd2 = [
                "gcloud", "compute", "instances", "list",
                "--filter=name:php-instance-*", 
                "--format=json"
            ]
            result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=30)
            if result2.returncode == 0:
                instances = json.loads(result2.stdout)
                print(f"DEBUG: Found {len(instances)} instances via direct list", file=sys.stderr)
        
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
        
        for instance in instances:
            instance_name = ""
            if "instance" in instance:
                # From MIG list
                instance_name = instance["instance"].split("/")[-1]
            else:
                # From direct instances list
                instance_name = instance["name"]
            
            print(f"DEBUG: Processing instance: {instance_name}", file=sys.stderr)
            
            # Get instance details to find external IP
            ip_cmd = [
                "gcloud", "compute", "instances", "describe", instance_name,
                "--zone=us-central1-f", "--format=json"
            ]
            ip_result = subprocess.run(ip_cmd, capture_output=True, text=True, timeout=30)
            
            if ip_result.returncode == 0:
                instance_details = json.loads(ip_result.stdout)
                # Extract external IP
                for interface in instance_details.get("networkInterfaces", []):
                    for config in interface.get("accessConfigs", []):
                        if "natIP" in config and config["natIP"]:
                            ip = config["natIP"]
                            inventory["php_servers"]["hosts"].append(ip)
                            print(f"DEBUG: Added instance {instance_name} with IP {ip}", file=sys.stderr)
                            break
        
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
