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
                        busybox unzip -o terraform_1.5.7_linux_amd64.zip 
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
        

        stage('Ansible Deploy') {
            steps {
                dir('php-deploy') {
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                        
                        # Get the zone dynamically
                        ZONE=$(gcloud compute instances list --filter="name:ansible-master" --format="value(ZONE)" --project=siva-477505)
                        
                        # Copy ansible files to Ansible master
                        gcloud compute scp --recurse ansible/ ansible-master:~/ --zone=${ZONE} --project=siva-477505
                        
                        # Run Ansible playbook
                        gcloud compute ssh ansible-master \
                        --zone=us-central1-a \
                        --project=siva-477505 \
                        --command="cd ~/ansible && chmod +x inventory-gcp.py && ansible-playbook -i ./inventory-gcp.py deploy-php.yml"

                     #   gcloud compute ssh ansible-master --zone=${ZONE} --project=siva-477505 --command='
                     #       cd ~/ansible
                     #       chmod +x inventory-gcp.py
                     #       ansible-playbook -i inventory-gcp.py deploy-php.yml
                     #   '
                    '''
                }
            }
        }
        
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
