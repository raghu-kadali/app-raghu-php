pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Terraform') {
            steps {
                sh '''
                    # Install Terraform
                    wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    sudo unzip terraform_1.5.7_linux_amd64.zip -d /usr/local/bin/
                    sudo chmod +x /usr/local/bin/terraform
                    rm terraform_1.5.7_linux_amd64.zip
                    terraform --version
                '''
            }
        }
        stage('Terraform Setup') {
            steps {
                sh 'terraform init -input=false'
            }
        }
        stage('Terraform Apply') {
            steps {
                sh 'terraform apply -auto-approve'
            }
        }
    }
}
