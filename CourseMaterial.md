# OpsBoard — 12 Week Cloud + DevOps Course

## Project Theme

### **OpsBoard — Internal Incident & Task Tracking SaaS**

A realistic internal tool for operations teams.

### Core Features
- User authentication  
- Create / assign / track incidents  
- Status lifecycle (open → in_progress → resolved)  
- Basic analytics (counts, rates)  

---

## Final System (Target)

- REST API (users + incidents)
- PostgreSQL database
- Dockerized services
- AWS deployment
- Terraform-managed infrastructure
- CI/CD pipeline
- Monitoring (metrics + logs)
- Kubernetes deployment

---

# Month 1 — Build the Product Locally

## Week 1 — Core API

### Tasks

#### 1.1 Project Setup
- Initialize repository
- Choose stack (Node/Express or Python/FastAPI)
- Create project structure

#### 1.2 Health Endpoint
- `/health` → returns OK

#### 1.3 Incident Model
Fields:
- id
- title
- description
- status (open/in_progress/resolved)
- created_at

#### 1.4 CRUD Endpoints
- Create incident
- List incidents
- Update status
- Delete incident

#### 1.5 In-Memory Storage
- Temporary storage for incidents

### Deliverable
- API runs locally
- CRUD works via curl/Postman

---

## Week 2 — Persistence + Auth

### Tasks

#### 2.1 PostgreSQL Setup
- Install and run locally

#### 2.2 Replace In-Memory Storage
- Store incidents in DB

#### 2.3 User Model
Fields:
- id
- email
- password (hashed)

#### 2.4 Authentication
- Register endpoint
- Login endpoint
- JWT token

#### 2.5 Ownership
- Link incidents to users

### Deliverable
- Authenticated users manage their own incidents

---

## Week 3 — Networking Layer

### Tasks

#### 3.1 Nginx Setup
- Reverse proxy `/api` → backend

#### 3.2 Domain Setup (Optional)
- Use hosts file or real domain

#### 3.3 HTTPS Preparation
- Plan TLS integration

### Deliverable
- API accessible through Nginx

---

## Week 4 — Dockerization

### Tasks

#### 4.1 Dockerfile
- Build API image
- Use multi-stage builds

#### 4.2 Docker Compose
- API + PostgreSQL services

#### 4.3 Environment Variables
- Configure DB connection

#### 4.4 Data Persistence
- Add volume for database

### Deliverable
- Full system runs with:


---

# Month 2 — Cloud + Automation

## Week 5 — AWS Deployment

### Tasks

#### 5.1 AWS Setup
- Create account

#### 5.2 EC2 Instance
- Launch Ubuntu instance

#### 5.3 Install Docker
- Prepare runtime environment

#### 5.4 Deploy App
- Run containers manually

### Deliverable
- API accessible via public IP

---

## Week 6 — Terraform

### Tasks

#### 6.1 Terraform Init
- Create project structure

#### 6.2 Define Infrastructure
- EC2 instance
- Security group

#### 6.3 Variables
- Region
- Instance type

#### 6.4 Lifecycle
- Apply and destroy infra

### Deliverable
- Full infrastructure managed via Terraform

---

## Week 7 — CI/CD Pipeline

### Tasks

#### 7.1 GitHub Actions Setup

#### 7.2 Pipeline Steps
- Install dependencies
- Run tests
- Build Docker image
- Push to registry

#### 7.3 Deployment Automation
- SSH into EC2
- Pull latest image
- Restart container

### Deliverable
- Commit triggers automatic deployment

---

## Week 8 — Observability

### Tasks

#### 8.1 Metrics Endpoint
- Track requests and latency

#### 8.2 Prometheus
- Collect metrics

#### 8.3 Grafana
- Visualize metrics

#### 8.4 Dashboard
- CPU usage
- Request rate

#### 8.5 Logging
- Structured logs

### Deliverable
- System is observable and debuggable

---

# Month 3 — Kubernetes + Production

## Week 9 — Kubernetes (Local)

### Tasks

#### 9.1 Install Cluster
- minikube or kind

#### 9.2 Deployment Config
- Create Deployment YAML

#### 9.3 Service Config
- Create Service YAML

#### 9.4 Deploy App

### Deliverable
- App runs in Kubernetes locally

---

## Week 10 — Kubernetes (Cloud)

### Tasks

#### 10.1 Managed Cluster
- Create EKS (or equivalent)

#### 10.2 kubectl Access

#### 10.3 Deploy Application

#### 10.4 Ingress
- Expose via HTTP endpoint

### Deliverable
- Public Kubernetes deployment

---

## Week 11 — Production Features

### Tasks

#### 11.1 ConfigMaps
- External configuration

#### 11.2 Secrets
- Store credentials securely

#### 11.3 Scaling
- Multiple replicas

#### 11.4 Rolling Updates
- Zero downtime deployment

### Deliverable
- Production-grade behavior

---

## Week 12 — Finalization

### Tasks

#### 12.1 Failure Testing
- Kill pods
- Stop services
- Observe recovery

#### 12.2 Feature Enhancements
- Add priority field (low/medium/high)
- Add filtering
- Improve timestamps

#### 12.3 Documentation

Create:

##### README
- Project description
- Setup instructions
- Deployment steps
- Design decisions

##### Architecture Diagram
- Request flow
- Infrastructure layout

#### 12.4 Presentation Prep
Be able to explain:
- Docker usage
- Terraform benefits
- Kubernetes role
- Design tradeoffs

---

# Final Deliverable

Repository includes:

- API code  
- Docker configuration  
- Terraform infrastructure  
- Kubernetes manifests  
- CI/CD pipeline  
- Monitoring setup  
- Documentation  

---

# Evaluation Criteria

You should be able to:

- Rebuild system from scratch in <1 hour  
- Explain full architecture clearly  
- Debug failures using logs and metrics  
- Deploy automatically via CI/CD  

---

# Optional Extensions

- JWT refresh tokens  
- Rate limiting  
- Redis caching  
- Basic frontend UI  
- AI-powered feature (e.g. incident summarization)  

---

# Outcome

A realistic, production-style SaaS system demonstrating:

- Cloud deployment skills  
- DevOps automation  
- Infrastructure management  
- System reliability  

This project directly maps to real-world DevOps and cloud engineering roles.