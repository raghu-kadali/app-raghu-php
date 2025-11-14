pipeline {
    agent any
    
    environment {
        // These will be set in Jenkins credentials
        GCP_PROJECT = credentials('gcp-project')
        GCP_SA_KEY = credentials('gcp-sa-key')
        TF_VARS_FILE = 'production.tfvars'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Terraform Setup') {
            steps {
                sh '''
                cd terraform
                terraform init -upgrade
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
