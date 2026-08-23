# Kubernetes Fundamentals

A minimal example app and Kubernetes manifests to demonstrate building, containerizing, and deploying a simple Python web application.

Contents
- app/: simple Flask app, Dockerfile, and Python deps
- k8s/: Kubernetes manifests (Deployment, Pod)

Prerequisites
- Docker
- kubectl configured for your cluster (or [minikube](https://minikube.sigs.k8s.io/) / kind)
- Python 3.9+ (for local runs)

Run locally
1. Create and activate a virtual environment (optional):

```
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies and run:

```
pip install -r app/requirements.txt
python app/app.py
```

Build and run with Docker

```
docker build -t kubernetes-fundamentals:latest -f app/Dockerfile app/
docker run -p 5000:5000 kubernetes-fundamentals:latest
```

Push to a registry (example for Docker Hub):

```
docker tag kubernetes-fundamentals:latest <your-dockerhub-username>/kubernetes-fundamentals:latest
docker push <your-dockerhub-username>/kubernetes-fundamentals:latest
```

Kubernetes deployment
Apply the manifests in the `k8s/` folder:

```
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/pod.yml
```

Check status:

```
kubectl get pods
kubectl get deployments
kubectl describe pod <pod-name>
```

Cleanup

```
kubectl delete -f k8s/pod.yml
kubectl delete -f k8s/deployment.yml
```

Notes
- Edit `k8s/deployment.yml` to point the image to your registry if you pushed a remote image.
- The `app/` folder contains the application entrypoint at `app/app.py` and `Dockerfile`.
