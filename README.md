# OpsBoard

OpsBoard is a small incident-tracking API built as a DevOps learning project. The product surface is intentionally simple: users register, log in, and manage their own incidents. The project focus is the operational path around the app: Docker, CI/CD, Terraform, AWS, Kubernetes, observability, and recovery.

## Stack

- FastAPI API
- PostgreSQL
- Docker and Docker Compose
- GitHub Actions
- GHCR container registry
- Terraform-managed EC2 baseline
- Kubernetes manifests for kind and EKS
- Prometheus metrics
- Grafana dashboards
- Structured JSON logs

## Local Docker Setup

Create a local env file:

```powershell
Copy-Item .env.example .env
```

Run the full local stack:

```powershell
docker compose up -d --build
```

Verify the API:

```powershell
curl http://localhost:8000/health
```

Useful local endpoints:

```text
API:        http://localhost:8000
Metrics:    http://localhost:8000/metrics
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
```

## Tests

The CI pipeline runs tests with a temporary PostgreSQL service container. Locally, run tests from a configured Python environment:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

## Container Image

GitHub Actions builds and pushes the API image to GHCR:

```text
ghcr.io/rokobata510/opsboard-api:latest
```

The production Docker Compose and Kubernetes manifests use that image rather than building the API on the target host.

## Local Kubernetes

This repo uses kind for local Kubernetes.

Create a cluster:

```powershell
kind create cluster --name opsboard
kubectl get nodes
```

Create the local-only secret from the example:

```powershell
Copy-Item k8s/secret.example.yml k8s/secret.yml
```

Edit `k8s/secret.yml` with local/dev values. This file is ignored by git.

Apply manifests:

```powershell
kubectl apply -f k8s/config.yml
kubectl apply -f k8s/secret.yml
kubectl apply -f k8s/postgres.yml
kubectl apply -f k8s/api-deployment.yml
kubectl apply -f k8s/api-service.yml
```

Test locally:

```powershell
kubectl port-forward service/opsboard-api 8000:8000
curl http://localhost:8000/health
```

## AWS EKS Deployment

Create the EKS cluster:

```powershell
eksctl create cluster -f eksctl/opsboard-cluster.yml
kubectl get nodes
```

Apply app manifests:

```powershell
kubectl apply -f k8s/config.yml
kubectl apply -f k8s/secret.yml
kubectl apply -f k8s/postgres.yml
kubectl apply -f k8s/api-deployment.yml
kubectl apply -f k8s/api-service-aws.yml
```

Find the public endpoint:

```powershell
kubectl get service opsboard-api-public
```

Test:

```powershell
curl http://YOUR_ELB_DNS/health
```

## Safety Notes

- Do not commit `.env`, `*.pem`, Terraform state, or `k8s/secret.yml`.
- `k8s/secret.example.yml` is safe to commit because it contains placeholders.
- The EKS cluster and AWS load balancer cost money while running.
- Delete the public load balancer when not needed:

```powershell
kubectl delete -f k8s/api-service-aws.yml
```

- Delete the EKS cluster when done:

```powershell
eksctl delete cluster -f eksctl/opsboard-cluster.yml
```

## Operational Docs

- [Architecture](docs/architecture.md)
- [Runbook](docs/runbook.md)
- [Presentation Notes](docs/presentation.md)
