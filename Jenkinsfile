pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "vishnuvardhandommeti/mini-k8s-demo:latest"
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

                    # Ensure Minikube is running, or start it
                    minikube status || minikube start --driver=docker --cpus=2 --memory=4096 --disk-size=10g
                    
                    # Set Minikube context for Jenkins
                    mkdir -p /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
                    sudo ln -sf $HOME/.kube/config /var/lib/jenkins/.kube/config
                    sudo ln -sf $HOME/.minikube /var/lib/jenkins/.minikube
                    sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
                    export KUBECONFIG=/var/lib/jenkins/.kube/config
                    kubectl config use-context minikube

                    echo "Minikube setup complete!"
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
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
