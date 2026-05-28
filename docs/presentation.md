# OpsBoard Presentation Notes

## One-Minute Summary

OpsBoard is an incident-tracking API used to demonstrate a realistic DevOps path: local API development, Dockerization, AWS deployment, Terraform-managed infrastructure, CI/CD, observability, local Kubernetes, and EKS deployment.

## What The App Does

- Users register and log in.
- Authenticated users create, list, update, and delete their own incidents.
- The API exposes health and metrics endpoints.

## Docker Usage

Docker packages the FastAPI API into a repeatable image. Docker Compose runs the local multi-service system:

```text
API
Postgres
Prometheus
Grafana
```

## Terraform Benefits

Terraform was used to codify the EC2 baseline infrastructure:

```text
region
EC2 instance
security group
root volume
outputs
```

The key benefit is reproducibility: infrastructure can be reviewed, recreated, and destroyed from code rather than console clicks.

## CI/CD

GitHub Actions handles:

```text
dependency install
test database setup
pytest
Docker build
push to GHCR
deployment automation
```

This catches missing dependencies and broken Docker builds before deployment.

## Observability

The API exposes Prometheus metrics at:

```text
/metrics
```

Prometheus scrapes the API. Grafana visualizes request rate and latency. The API also emits structured JSON logs for request completion.

## Kubernetes Role

Kubernetes manages the running containers:

```text
API Deployment with 2 replicas
Postgres Deployment
Services for stable networking
ConfigMap for non-secret config
Secret for credentials
LoadBalancer Service for public AWS access
```

Kubernetes adds:

```text
self-healing
rolling updates
service discovery
replica management
health probes
```

## EKS

The cloud Kubernetes deployment runs on EKS in Frankfurt:

```text
cluster name: opsboard
region: eu-central-1
node group: opsboard-workers
node type: t3.medium
```

The public endpoint is created through a Kubernetes `LoadBalancer` Service.

## Design Tradeoffs

- Postgres runs inside Kubernetes for learning. For production, use RDS.
- The API has two replicas, but the database is still single-instance.
- Public HTTP uses a LoadBalancer Service without TLS. Production should add HTTPS and a real domain.
- Kubernetes Secret manifests are not a complete secret-management solution. Production should use AWS Secrets Manager or a sealed/external secret flow.
- The project favors clarity and learning over maximum production sophistication.

## Failure Testing Story

The final validation demonstrates:

```text
kill one API pod -> Kubernetes recreates it
kill Postgres pod -> Kubernetes recreates it
rollout restart API -> rolling update keeps service available
```

## Recovery Story

The repository contains the operating instructions and manifests needed to rebuild:

```text
Docker stack
kind cluster deployment
EKS cluster config
Kubernetes workloads
public service
observability stack
```

Secrets are intentionally excluded from git and recreated from templates.
