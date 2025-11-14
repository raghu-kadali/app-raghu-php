pipeline {
    agent any

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
                pwd
                ls -l
                terraform init 
                
                '''
            }
        }
        
        stage('Terraform Plan') {
            steps {
                sh '''
                cd terraform
                terraform plan -var-file=${TF_VARS_FILE} -out=tfplan
                '''
            }
        }
        
        stage('Terraform Apply') {
            steps {
                sh '''
                cd terraform
                terraform apply -auto-approve tfplan
                '''
            }
        }
        
        stage('Get Infrastructure Info') {
            steps {
                script {
                    dir('terraform') {
                        env.ANSIBLE_MASTER_IP = sh(
                            script: 'terraform output -raw ansible_master_ip',
                            returnStdout: true
                        ).trim()
                    }
                }
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
    
    }
