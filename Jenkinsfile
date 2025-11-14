pipeline {
    agent any
    
    environment {
        GCP_KEY = credentials('terraform')
    }

    stages {
        stage('Terraform Deploy') {
            steps {
                sh '''
                    git clone https://github.com/pavandath/php-deploy.git || true
                    cd php-deploy
                    
                    if [ ! -f "terraform" ]; then
                        wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                        busybox unzip -o terraform_1.5.7_linux_amd64.zip
                        chmod +x terraform
                        rm terraform_1.5.7_linux_amd64.zip
                    fi
                    
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
            
            # Find and run ansible
            gcloud compute ssh ubuntu@ansible-master --zone=us-central1-a --project=siva-477505 --command="find /home -name inventory-gcp.py -type f 2>/dev/null | head -1 | xargs dirname | xargs -I {} bash -c 'cd {} && chmod +x inventory-gcp.py && ansible-playbook -i inventory-gcp.py deploy-php.yml'" --ssh-flag="-o StrictHostKeyChecking=no"
        '''
    }
}
}
