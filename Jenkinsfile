pipeline {
    agent {
        docker {
            image 'hashicorp/terraform:latest'
            args '-v $WORKSPACE:/workspace -w /workspace'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('GCP Authentication') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account-key', variable: 'GCP_CREDENTIALS')]) {
                    sh '''
                        cp ${GCP_CREDENTIALS} /workspace/credentials.json
                        export GOOGLE_APPLICATION_CREDENTIALS=/workspace/credentials.json
                    '''
                }
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
