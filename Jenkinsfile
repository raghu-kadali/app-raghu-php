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
                    # Install Terraform without sudo
                    wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    unzip terraform_1.5.7_linux_amd64.zip -d $HOME/.local/bin/
                    mkdir -p $HOME/.local/bin
                    chmod +x $HOME/.local/bin/terraform
                    export PATH="$HOME/.local/bin:$PATH"
                    rm terraform_1.5.7_linux_amd64.zip
                    terraform --version
                '''
            }
        }
        stage('Terraform Setup') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    terraform init -input=false
                '''
            }
        }
        stage('Terraform Apply') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    terraform apply -auto-approve
                '''
            }
        }
    }
}
