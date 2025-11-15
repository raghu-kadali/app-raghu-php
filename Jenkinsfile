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
                    sh '''
                        wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                        busybox unzip -o terraform_1.5.7_linux_amd64.zip
                        chmod +x terraform
                        rm terraform_1.5.7_linux_amd64.zip
                    '''
                }
            }
        }
        
        stage('User Approval') {
            steps {
                script {
                    def userInput = input(
                        id: 'userInput',
                        message: 'Proceed with Terraform deployment?',
                        parameters: [
                            choice(
                                name: 'ACTION',
                                choices: ['apply', 'destroy', 'cancel'],
                                description: 'Choose Terraform action'
                            ),
                            string(
                                name: 'ENVIRONMENT',
                                defaultValue: 'production',
                                description: 'Deployment environment'
                            )
                        ]
                    )
                    env.TF_ACTION = userInput.ACTION
                    env.DEPLOY_ENV = userInput.ENVIRONMENT
                }
            }
        }
        
        stage('terraform deploy') {
            when {
                expression { env.TF_ACTION == 'apply' }
            }
            steps {
                dir('php-deploy') {
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        ./terraform init
                        ./terraform apply -auto-approve
                    '''
                }
            }
        }
        
        stage('terraform destroy') {
            when {
                expression { env.TF_ACTION == 'destroy' }
            }
            steps {
                dir('php-deploy') {
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}

                        ./terraform destroy -auto-approve
                    '''
                }
            }
        }
    }
}
