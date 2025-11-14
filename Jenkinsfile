pipeline {
    agent any

    stages {
        stage('Terraform Deploy Infrastructure') {
            steps {
                withCredentials([file(credentialsId: 'terraform', variable: 'GCP_KEY')]) {
                    sh '''
                        rm -rf php-deploy
                        git clone https://github.com/pavandath/php-deploy.git
                        cd php-deploy
                        
                        # Download and setup Terraform
                        wget -q https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip
                        busybox unzip -o terraform_1.5.7_linux_amd64.zip
                        chmod +x terraform
                        rm terraform_1.5.7_linux_amd64.zip
                        
                        # Use environment variable for Terraform
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        
                        ./terraform destroy --auto-approve
                        
                    '''
                }
            }
        }

        
    }

}
