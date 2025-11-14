#!/usr/bin/env python3
import subprocess
import json
import sys

def get_instances():
    cmd = [
        'gcloud', 'compute', 'instances', 'list',
        '--format=json',
        '--filter=tags.items=php-app'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    instances = json.loads(result.stdout)
    
    inventory = {
        "web_servers": {
            "hosts": [],
            "vars": {
                "ansible_user": "ubuntu",
                "ansible_ssh_private_key_file": "~/ansible/key.pem"  # Make sure this key exists
            }
        }
    }
    
    for instance in instances:
        # Use external IP instead of internal hostname
        for interface in instance.get('networkInterfaces', []):
            for config in interface.get('accessConfigs', []):
                if 'natIP' in config:
                    inventory["web_servers"]["hosts"].append(config['natIP'])
    
    return inventory

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(json.dumps(get_instances()))
    else:
        print(json.dumps({}))
