pipeline {
    agent any
    
    environment {
        GCP_KEY = credentials('terraform')
    }

    stages {
        stage('Terraform install') {
            steps {
                sh '''
                    rm -rf php-deploy
                    git clone https://github.com/pavandath/php-deploy.git || true
                   '''
                dir('php-deploy'){  
                    wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                    busybox unzip -o terraform_1.5.7_linux_amd64.zip
                    chmod +x terraform
                    rm terraform_1.5.7_linux_amd64.zip
                }
          
            }
        }
        stage('terraform deploy'){
            steps {
                dir('php-deploy'){
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        ./terraform init
                        ./terraform apply -auto-approve
                    '''
                }
            }
        }
       

    }
}
