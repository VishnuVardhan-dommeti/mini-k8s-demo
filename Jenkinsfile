pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "vishnuvardhandommeti/mini-k8s-demo:latest"
        MINIKUBE_HOME = "/var/lib/jenkins/.minikube"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    retry(3) {
                        checkout([$class: 'GitSCM', 
                            branches: [[name: '*/main']], 
                            userRemoteConfigs: [[url: 'https://github.com/VishnuVardhan-dommeti/mini-k8s-demo.git']]
                        ])
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE app/'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        sh 'docker push vishnuvardhandommeti/mini-k8s-demo:latest'
                    }
                }
            }
        }

        stage('Configure Minikube') {
            steps {
                script {
                    sh '''
                        echo "Setting up Minikube for Jenkins..."

                        # Fix file permissions for Minikube & Kube config
                        sudo mkdir -p /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
                        sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
                        sudo chmod -R 777 /var/lib/jenkins/.kube /var/lib/jenkins/.minikube

                        # Set Minikube environment variables
                        export MINIKUBE_HOME=/var/lib/jenkins/.minikube
                        export KUBECONFIG=/var/lib/jenkins/.kube/config
                        sudo chmod 600 $KUBECONFIG

                        # Delete old Minikube instance if present
                        sudo minikube delete || true

                        # Start Minikube with proper settings
                        sudo sysctl fs.protected_regular=0
                        minikube start --driver=docker --cpus=2 --memory=4096 --disk-size=10g --force --wait=all

                        # Update kubectl context
                        minikube update-context
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh '''
                        echo "Deploying to Minikube..."
                        export KUBECONFIG=/var/lib/jenkins/.kube/config
                        
                        # Ensure correct permissions for kubeconfig
                        sudo chmod 600 /var/lib/jenkins/.kube/config

                        # Apply Kubernetes manifests
                        kubectl apply -f k8s/namespace.yaml
                        kubectl apply -f k8s/configmap.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml

                        # Wait for deployment rollout
                        kubectl -n mini-demo rollout status deployment/flask-app

                        # Get Minikube service URL
                        minikube service flask-app -n mini-demo --url
                    '''
                }
            }
        }
    }
}
