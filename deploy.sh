#!/bin/bash
minikube start
eval $(minikube docker-env)
docker build -t mini-k8s-demo:latest app/
kubectl apply -f k8s/
minikube service flask-app -n mini-demo --url
