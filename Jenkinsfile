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

                        # Fix file lock issue
                        sudo sysctl fs.protected_regular=0

                        # Ensure Jenkins has access to Minikube directories
                        sudo mkdir -p /var/lib/jenkins/.kube /var/lib/jenkins/.minikube

                        # Fix symlink issues
                        if [ ! -f /var/lib/jenkins/.kube/config ]; then
                            sudo ln -sf /home/mthree/.kube/config /var/lib/jenkins/.kube/config
                        fi

                        if [ ! -L /var/lib/jenkins/.minikube ]; then
                            sudo ln -sf /home/mthree/.minikube /var/lib/jenkins/.minikube
                        fi

                        # Fix permissions for Jenkins
                        sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
                        sudo chmod -R u+wrx /var/lib/jenkins/.kube /var/lib/jenkins/.minikube

                        # Explicitly set KUBECONFIG
                        export KUBECONFIG=/var/lib/jenkins/.kube/config
                        sudo chmod 600 $KUBECONFIG

                        # Clean existing Minikube and restart
                        sudo minikube delete || true

                        # Start Minikube inside Jenkins with force and waiting for API server
                        export MINIKUBE_HOME=/var/lib/jenkins/.minikube
                        sudo minikube start --driver=docker --cpus=2 --memory=4096 --disk-size=10g --force --wait=all
                        sudo minikube update-context
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh '''
                        export KUBECONFIG=/var/lib/jenkins/.kube/config
                        kubectl apply -f k8s/namespace.yaml
                        kubectl apply -f k8s/configmap.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl -n mini-demo rollout status deployment/flask-app
                        minikube service flask-app -n mini-demo --url
                    '''
                }
            }
        }
    }
}
