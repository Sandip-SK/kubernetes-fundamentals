# Kubernetes Fundamentals

This project demonstrates a simple Flask application deployed on Kubernetes with common production-style resources such as health probes, autoscaling, ingress, secrets, config maps, persistent storage, and resilience policies.

## Project structure

- `app/app.py` – Flask API with `/` and `/health` endpoints
- `app/Dockerfile` – container image definition
- `app/requirements.txt` – Python dependencies
- `k8s/` – Kubernetes manifests for deployment, networking, scaling, configuration, and storage

## Application behavior

The Python app exposes:

- `/` → returns a JSON message and hostname
- `/health` → returns `{"status": "healthy"}`

This makes it suitable for Kubernetes startup, readiness, and liveness probes.

## Prerequisites

- Docker
- `kubectl` configured to a cluster
- Python 3.9+
- Optional: NGINX Ingress Controller for the Ingress manifest

## Run locally

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies and run the app:

```bash
pip install -r app/requirements.txt
python app/app.py
```

3. Test locally:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

## Build and run with Docker

```bash
docker build -t kubernetes-fundamentals:2.0 -f app/Dockerfile app/
docker run -p 5000:5000 kubernetes-fundamentals:2.0
```

## Kubernetes deployment

Apply the manifests in the order below:

```bash
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secret.yml
kubectl apply -f k8s/postgres-pvc.yml
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
kubectl apply -f k8s/ingress.yml
kubectl apply -f k8s/hpa.yml
kubectl apply -f k8s/pdb.yml
kubectl apply -f k8s/allow-only-testclient-np.yml
```

Optional storage demonstration pod:

```bash
kubectl apply -f k8s/storage-test.yml
```

To test a workload with resource pressure:

```bash
kubectl apply -f k8s/pending-pod.yml
```

## Check workload status

```bash
kubectl get pods
kubectl get deploy
kubectl get svc
kubectl get ingress
kubectl get hpa
kubectl describe pod <pod-name>
```

## Accessing the app

The Ingress manifest routes requests for `api.local` to the service.

If you are using a local cluster with ingress support, add an entry such as:

```text
127.0.0.1 api.local
```

Then open:

```text
http://api.local/
```

You can also port-forward directly to the service for testing:

```bash
kubectl port-forward service/kubernetes-fundamentals 8080:80
curl http://localhost:8080/
```

## Included Kubernetes features

This repository includes examples for:

- RollingUpdate deployments
- Liveness and readiness probes
- Resource requests and limits
- ConfigMaps and Secrets
- ClusterIP Service
- Ingress routing
- HorizontalPodAutoscaler
- PodDisruptionBudget
- NetworkPolicy
- PersistentVolumeClaim attached to a test pod

## Cleanup

```bash
kubectl delete -f k8s/ingress.yml
kubectl delete -f k8s/service.yml
kubectl delete -f k8s/deployment.yml
kubectl delete -f k8s/hpa.yml
kubectl delete -f k8s/pdb.yml
kubectl delete -f k8s/allow-only-testclient-np.yml
kubectl delete -f k8s/configmap.yml
kubectl delete -f k8s/secret.yml
kubectl delete -f k8s/postgres-pvc.yml
kubectl delete -f k8s/storage-test.yml
kubectl delete -f k8s/pending-pod.yml
```

## Notes

- Update `k8s/deployment.yml` to point to your own image if you push it to a registry.
- Secret values in `k8s/secret.yml` should be populated before real use.
- The project is intended as a learning-focused example for Kubernetes fundamentals and common deployment patterns.
