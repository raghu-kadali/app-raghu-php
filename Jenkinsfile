pipeline {
    agent any
    stages {
        stage('Terraform Deploy') {
            steps {
                sh '''
                    rm -rf php-deploy
                    git clone https://github.com/pavandath/php-deploy.git
                    cd php-deploy
                    
                    # Download Terraform
                    wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    busybox unzip -o terraform_1.5.7_linux_amd64.zip
                    chmod +x terraform
                    rm terraform_1.5.7_linux_amd64.zip
                    
                    # Authenticate with the service account (now it has permissions!)
                    gcloud auth activate-service-account --key-file=/var/lib/jenkins/terraform-key.json
                    gcloud config set project siva-477505
                    
                    # Run Terraform
                    ./terraform init
                    ./terraform apply -auto-approve
                '''
            }
        }
    }
}
