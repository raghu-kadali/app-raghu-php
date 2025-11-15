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
                    git clone https://github.com/raghu-kadali/app-raghu-php.git || true
                '''
                dir('php-deploy'){  
                    sh '''
                        wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                        busybox unzip -o terraform_1.5.7_linux_amd64.zip
                        chmod +x terraform
                        rm terraform_1.5.7_linux_amd64.zip
                    '''
                }
            }
        }
        
        stage('terraform apply') {
            steps {
                dir('php-deploy') {
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        ./terraform init
                        ./terraform apply -auto-approve -lock=false
                    '''
                }
            }
        }
        
        stage('Destroy Confirmation') {
            steps {
                script {
                    def destroy = input(
                        message: 'Do you want to destroy the infrastructure?', 
                        parameters: [
                            choice(choices: ['no', 'yes'], description: 'Select action', name: 'DESTROY')
                        ]
                    )
                    if (destroy == 'yes') {
                        dir('php-deploy') {
                            sh '''
                                export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                                ./terraform destroy -auto-approve -lock=false
                            '''
                        }
                    }
                }
            }
        }
    }
}
