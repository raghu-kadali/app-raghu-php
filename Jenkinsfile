pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Download Terraform') {
            steps {
                sh '''
                    # Download terraform
                    wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    
                    # Use full path to unzip
                    /usr/bin/unzip -o terraform_1.5.7_linux_amd64.zip
                    
                    chmod +x terraform
                    ./terraform --version
                    rm terraform_1.5.7_linux_amd64.zip
                '''
            }
        }
        stage('Terraform Setup') {
            steps {
                sh './terraform init -input=false'
            }
        }
        stage('Terraform Apply') {
            steps {
                sh './terraform apply -auto-approve'
            }
        }
    }
}
