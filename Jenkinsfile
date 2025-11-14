pipeline {
    agent any
    
    environment {
        GCP_KEY = credentials('terraform')
        GCP_PROJECT = 'siva-477505'
        TF_VERSION = '1.5.7'
    }

    stages {
        stage('Terraform Deploy') {
            steps {
                sh '''
                    rm -rf php-deploy
                    git clone https://github.com/pavandath/php-deploy.git || true
                    cd php-deploy
                    
                    wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    busybox unzip -o terraform_1.5.7_linux_amd64.zip
                    chmod +x terraform
                    rm terraform_1.5.7_linux_amd64.zip
                    
                    export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                    ./terraform init
                    ./terraform apply -auto-approve
                '''
            }
        }
        
        stage('Ansible Deploy') {
            steps {
                sshagent(['ansible-master-ssh-key']) {
                    sh '''
                        cd php-deploy
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        ANSIBLE_MASTER_IP=$(gcloud compute instances list --filter="name:ansible-master" --format="value(EXTERNAL_IP)" --project=siva-477505)
                        
                        # Copy the entire ansible directory to Ansible master
                        scp -o StrictHostKeyChecking=no -r ansible/ ubuntu@${ANSIBLE_MASTER_IP}:~/
                        
                        # Now SSH and run ansible-playbook from the copied directory
                        ssh -o StrictHostKeyChecking=no ubuntu@${ANSIBLE_MASTER_IP} '
                            cd ~/ansible
                            chmod +x inventory-gcp.py
                            ansible-playbook -i inventory-gcp.py deploy-php.yml
                        '
                    '''
                }
            }
        }
    }
}
