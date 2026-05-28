# OpsBoard Runbook

## Quick Health Check

Check Kubernetes context:

```powershell
kubectl config current-context
```

Check workloads:

```powershell
kubectl get pods
kubectl get deployments
kubectl get services
```

Check public API:

```powershell
kubectl get service opsboard-api-public
curl http://YOUR_ELB_DNS/health
```

Expected response:

```json
{"status":"OK","updated":"yupp"}
```

## Logs

API logs:

```powershell
kubectl logs deployment/opsboard-api
```

Follow logs:

```powershell
kubectl logs deployment/opsboard-api -f
```

Postgres logs:

```powershell
kubectl logs deployment/postgres
```

## Failure Test: Kill API Pod

List API pods:

```powershell
kubectl get pods -l app=opsboard-api
```

Delete one pod:

```powershell
kubectl delete pod POD_NAME
```

Observe recovery:

```powershell
kubectl get pods -l app=opsboard-api --watch
```

Expected result:

```text
Kubernetes creates a replacement pod.
The public endpoint remains available through the other API pod.
```

## Failure Test: Kill Postgres Pod

List Postgres pods:

```powershell
kubectl get pods -l app=postgres
```

Delete the pod:

```powershell
kubectl delete pod POD_NAME
```

Observe recovery:

```powershell
kubectl get pods -l app=postgres --watch
```

Expected result:

```text
Kubernetes recreates the Postgres pod.
```

Important limitation:

```text
The demo Postgres deployment does not use a PersistentVolumeClaim.
For production, use RDS or persistent Kubernetes storage.
```

## Rolling Update Test

Restart API deployment:

```powershell
kubectl rollout restart deployment/opsboard-api
kubectl rollout status deployment/opsboard-api
```

Watch pods:

```powershell
kubectl get pods -l app=opsboard-api --watch
```

Expected result:

```text
Kubernetes starts replacement pods before removing old ready pods.
The service should remain available.
```

## Rollback

View rollout history:

```powershell
kubectl rollout history deployment/opsboard-api
```

Rollback to previous revision:

```powershell
kubectl rollout undo deployment/opsboard-api
kubectl rollout status deployment/opsboard-api
```

## Common Debug Commands

Describe deployment:

```powershell
kubectl describe deployment opsboard-api
```

Describe a pod:

```powershell
kubectl describe pod POD_NAME
```

Inspect events:

```powershell
kubectl get events --sort-by=.lastTimestamp
```

Check endpoints selected by a Service:

```powershell
kubectl get endpoints opsboard-api-public
kubectl get endpoints postgres
```

## Cost Control

Delete only the public load balancer:

```powershell
kubectl delete -f k8s/api-service-aws.yml
```

Recreate it later:

```powershell
kubectl apply -f k8s/api-service-aws.yml
```

Delete the whole EKS cluster:

```powershell
eksctl delete cluster -f eksctl/opsboard-cluster.yml
```

Check for remaining AWS costs:

```powershell
aws ec2 describe-load-balancers
aws ec2 describe-instances --region eu-central-1
aws ec2 describe-volumes --region eu-central-1
```
