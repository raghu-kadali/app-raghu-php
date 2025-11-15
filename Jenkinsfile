pipeline {
    agent any
    
    environment {
        GCP_KEY = credentials('terraform')
    }

    stages {
        stage('Terraform Install') {
            steps {
                sh '''
                    rm -rf php-deploy
                    git clone https://github.com/pavandath/php-deploy.git
                '''
                dir('php-deploy'){  
                    sh '''
                        wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                        unzip -o terraform_1.5.7_linux_amd64.zip
                        chmod +x terraform
                        rm terraform_1.5.7_linux_amd64.zip
                    '''
                }
            }
        }
        
        stage('Terraform Deploy') {
            steps {
                dir('php-deploy') {
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        ./terraform init -input=false
                        ./terraform apply -auto-approve -input=false
                    '''
                }
            }
        }
        
        stage('Destroy Infrastructure?') {
            steps {
                script {
                    def userInput = input(
                        id: 'userInput', 
                        message: 'Do you want to DESTROY the infrastructure?', 
                        parameters: [
                            choice(
                                name: 'destroy',
                                choices: ['NO', 'YES'],
                                description: 'Select YES to destroy all resources'
                            )
                        ]
                    )
                    
                    if (userInput == 'YES') {
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
    }
}
