pipeline {
    agent any
    stages {
        stage('Download Terraform') {
            steps {
                sh '''
                    wget -O terraform.zip https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    unzip -o terraform.zip
                    chmod +x terraform
                    ./terraform --version
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
