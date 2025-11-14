pipeline {
    agent any
    
    environment {
        GCP_KEY = credentials('terraform')
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
        sh '''
            cd php-deploy
            export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
            ANSIBLE_MASTER_IP=$(gcloud compute instances list --filter="name:ansible-master" --format="value(EXTERNAL_IP)" --project=siva-477505)
            
            echo "Connecting to Ansible Master at: ${ANSIBLE_MASTER_IP}"
            
            # Copy ansible files using the external IP
            scp -o StrictHostKeyChecking=no -r ansible/ ubuntu@${ANSIBLE_MASTER_IP}:~/
            
            # SSH using the external IP
            ssh -o StrictHostKeyChecking=no ubuntu@${ANSIBLE_MASTER_IP} "
                cd ~/ansible
                chmod +x inventory-gcp.py
                ansible-playbook -i inventory-gcp.py deploy-php.yml
            "
        '''
    }
}
    }
}
