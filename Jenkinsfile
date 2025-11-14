pipeline {
    agent any
    stages {
        stage('Clean Existing Resources') {
            steps {
                withCredentials([file(credentialsId: 'terraform', variable: 'GCP_KEY')]) {
                    sh '''
                        gcloud auth activate-service-account --key-file=${GCP_KEY}
                        gcloud config set project siva-477505
                        
                        # Delete the existing service account
                        gcloud iam service-accounts delete php-instance@siva-477505.iam.gserviceaccount.com --quiet || echo "Service account already deleted or doesn't exist"
                    '''
                }
            }
        }
        stage('Terraform Deploy') {
            steps {
                withCredentials([file(credentialsId: 'terraform', variable: 'GCP_KEY')]) {
                    sh '''
                        rm -rf php-deploy
                        git clone https://github.com/pavandath/php-deploy.git
                        cd php-deploy
                        
                        wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                        busybox unzip -o terraform_1.5.7_linux_amd64.zip
                        chmod +x terraform
                        rm terraform_1.5.7_linux_amd64.zip
                        
                        gcloud auth activate-service-account --key-file=${GCP_KEY}
                        gcloud config set project siva-477505
                        
                        ./terraform init
                        ./terraform apply -auto-approve
                    '''
                }
            }
        }
    }
}
