pipeline {
    agent any
    environment {
        TERRAFORM = '/usr/bin/terraform'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'rm -rf php-deploy || true'
            }
        }
        
        stage('Terraform Setup') {
            steps {
                sh '''
            
                ${TERRAFORM} init 
                '''
            }
        }
        
     
        }
        
        stage('Terraform Apply') {
            steps {
                sh '''
           
                ${TERRAFORM} apply -auto-approve 
                '''
            }
        }
        
 
        
        stage('Deploy Application') {
            steps {
                script {
                    sshagent(['ansible-master-ssh-key']) {
                        sh """
                        # Copy from ansible/ folder in workspace
                        scp -o StrictHostKeyChecking=no ./ansible/inventory-gcp.py ubuntu@${ANSIBLE_MASTER_IP}:~/
                        scp -o StrictHostKeyChecking=no ./ansible/deploy-php.yml ubuntu@${ANSIBLE_MASTER_IP}:~/
                        
                        # Execute deployment
                        ssh -o StrictHostKeyChecking=no ubuntu@${ANSIBLE_MASTER_IP} '
                            chmod +x inventory-gcp.py
                            ansible-playbook -i inventory-gcp.py deploy-php.yml
                        '
                        """
                    }
                }
            }
        }
        
    }
    
