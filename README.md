# 🐍 ALX Backend Python - Advanced Development Suite

A comprehensive collection of advanced Python projects covering generators, decorators, async programming, Django middleware, ORM signals, and Kubernetes orchestration. Built for scalable, production-ready backend systems.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)

---

## 📋 Repository Overview

This repository represents a complete journey through **advanced Python backend development**, from efficient data processing with generators to container orchestration with Kubernetes. Each directory contains a self-contained project module focusing on specific backend engineering concepts.

### 🎯 Core Learning Tracks

1. **🔄 Python Generators** - Memory-efficient data processing
2. **🎨 Python Decorators** - Function enhancement and metaprogramming
3. **⚡ Async Programming** - Concurrent operations and non-blocking I/O
4. **🛡️ Django Middleware** - Request/response processing pipelines
5. **📡 Django ORM Signals** - Event-driven database operations
6. **🐳 Container Orchestration** - Kubernetes deployment and scaling
7. **🧪 Testing & Integration** - Unit tests and integration workflows

---

## 📁 Project Structure

```
alx-backend-python/
├── python-generators-0x00/          # Memory-efficient data streaming
├── python-decorators-0x01/          # Function wrappers and metaprogramming
├── python-context-async-perations-0x02/  # Async/await patterns
├── Django-Middleware-0x03/          # Custom middleware implementation
├── Django-signals_orm-0x04/         # ORM event handling
├── messaging_app/                   # Kubernetes-orchestrated Django app
│   ├── kurbeScript                  # Cluster setup script
│   ├── deployment.yaml              # K8s deployment config
│   ├── blue_deployment.yaml         # Blue-green deployment
│   ├── green_deployment.yaml        # Green version deployment
│   ├── kubeservice.yaml             # Service configuration
│   ├── ingress.yaml                 # Ingress controller config
│   ├── kubctl-0x01                  # Scaling script
│   ├── kubctl-0x02                  # Blue-green deployment script
│   └── kubctl-0x03                  # Rolling update script
├── 0x03-Unittests_and_integration_tests/  # Testing strategies
├── venv/                            # Python virtual environment
├── .gitignore                       # Git ignore rules
├── manage                           # Django management script
├── settings                         # Configuration settings
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **MySQL 8.0+**
- **Docker** & **Docker Compose**
- **Minikube** (for Kubernetes)
- **kubectl** (Kubernetes CLI)
- **Git**

### Installation

```bash
# Clone the repository
git clone https://github.com/Dwaynemaster007/alx-backend-python.git
cd alx-backend-python

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up database (for generator projects)
python seed.py
```

---

## 📚 Project Modules

### 🔄 1. Python Generators (python-generators-0x00)

**Master memory-efficient data processing with Python generators.**

#### Key Features:
- Stream database rows one-by-one using `yield`
- Batch processing for large datasets
- Lazy pagination implementation
- Aggregate computations without loading full datasets

#### Core Files:
- `seed.py` - Database setup and population
- `0-stream_users.py` - Stream users from database
- `1-batch_processing.py` - Process data in batches
- `2-lazy_paginate.py` - Lazy loading pagination
- `4-stream_ages.py` - Memory-efficient aggregate functions

#### Learning Outcomes:
✅ Understand generator functions and `yield` keyword  
✅ Implement lazy evaluation for scalability  
✅ Handle large datasets without memory overflow  
✅ Build efficient database streaming solutions

---

### 🎨 2. Python Decorators (python-decorators-0x01)

**Enhance functions with decorator patterns and metaprogramming.**

#### Key Concepts:
- Function wrappers and closures
- Class-based decorators
- Decorator chaining
- Property decorators and descriptors

#### Learning Outcomes:
✅ Create reusable function enhancers  
✅ Implement authentication decorators  
✅ Build logging and timing wrappers  
✅ Master Python metaprogramming patterns

---

### ⚡ 3. Async Programming (python-context-async-perations-0x02)

**Build concurrent applications with async/await patterns.**

#### Key Features:
- Asynchronous context managers
- Non-blocking I/O operations
- Concurrent API calls
- Event loop management

#### Learning Outcomes:
✅ Write async functions with `async/await`  
✅ Implement context managers with `async with`  
✅ Handle concurrent operations efficiently  
✅ Optimize I/O-bound tasks

---

### 🛡️ 4. Django Middleware (Django-Middleware-0x03)

**Implement custom request/response processing pipelines.**

#### Key Features:
- Custom middleware classes
- Request preprocessing
- Response modification
- Authentication middleware

#### Learning Outcomes:
✅ Understand Django middleware lifecycle  
✅ Create custom middleware components  
✅ Implement cross-cutting concerns  
✅ Build authentication and logging middleware

---

### 📡 5. Django ORM Signals (Django-signals_orm-0x04)

**Build event-driven database operations with Django signals.**

#### Key Features:
- Pre-save and post-save signals
- Database event handling
- Decoupled application logic
- Signal receivers

#### Learning Outcomes:
✅ Implement Django signal handlers  
✅ Create event-driven architectures  
✅ Decouple business logic  
✅ Build auditing and logging systems

---

### 🐳 6. Container Orchestration with Kubernetes (messaging_app/)

**Deploy and manage containerized Django applications at scale.**

#### Project Overview:
Complete Kubernetes implementation featuring cluster setup, deployment strategies, scaling, and zero-downtime updates.

#### Components:

**📜 Configuration Files:**
- `deployment.yaml` - Initial deployment configuration
- `blue_deployment.yaml` - Blue environment (v1.0)
- `green_deployment.yaml` - Green environment (v2.0)
- `kubeservice.yaml` - Service definitions for traffic routing
- `ingress.yaml` - External access configuration

**🔧 Automation Scripts:**
- `kurbeScript` - Cluster initialization and verification
- `kubctl-0x01` - Scaling and load testing
- `kubctl-0x02` - Blue-green deployment execution
- `kubctl-0x03` - Rolling update automation

#### Task Breakdown:

**Task 0: Cluster Setup**
```bash
./kurbeScript
# - Starts Minikube cluster
# - Verifies cluster status
# - Lists available pods
```

**Task 1: Initial Deployment**
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs <pod-name>
```

**Task 2: Horizontal Scaling**
```bash
./kubctl-0x01
# - Scales to 3 replicas
# - Performs load testing with wrk
# - Monitors resource usage
```

**Task 3: Ingress Configuration**
```bash
# Install Nginx Ingress Controller
kubectl apply -f ingress.yaml
# See commands.txt for detailed steps
```

**Task 4: Blue-Green Deployment**
```bash
./kubctl-0x02
# - Deploys blue and green versions
# - Switches traffic gradually
# - Checks logs for errors
```

**Task 5: Rolling Updates**
```bash
./kubctl-0x03
# - Updates to v2.0 with zero downtime
# - Monitors rollout status
# - Tests with continuous curl requests
# - Verifies pod updates
```

#### Learning Outcomes:
✅ Set up local Kubernetes clusters with Minikube  
✅ Deploy containerized Django applications  
✅ Scale applications horizontally  
✅ Implement zero-downtime deployment strategies  
✅ Configure Ingress for external access  
✅ Perform blue-green and rolling deployments  
✅ Monitor and troubleshoot Kubernetes resources  
✅ Apply DevOps best practices

#### Kubernetes Best Practices Implemented:
- 📝 Declarative YAML configurations
- 🏷️ Strategic use of labels and selectors
- 🔍 Health checks (liveness & readiness probes)
- 📊 Resource requests and limits
- 🔐 ConfigMaps and Secrets management
- 📈 Auto-scaling with HPA
- 🔄 Rolling updates for zero downtime

---

### 🧪 7. Unit Tests & Integration Tests (0x03-Unittests_and_integration_tests/)

**Comprehensive testing strategies for robust applications.**

#### Learning Outcomes:
✅ Write unit tests with unittest framework  
✅ Implement integration tests  
✅ Mock external dependencies  
✅ Test coverage and quality assurance

---

## 🛠️ Common Commands

### Python Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

### Django Commands
```bash
# Run development server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Kubernetes Commands
```bash
# Start Minikube
minikube start

# Check cluster status
kubectl cluster-info

# List pods
kubectl get pods

# View pod logs
kubectl logs <pod-name>

# Scale deployment
kubectl scale deployment <name> --replicas=3

# Apply configuration
kubectl apply -f deployment.yaml

# Check rollout status
kubectl rollout status deployment/<name>

# View services
kubectl get services

# Monitor resource usage
kubectl top pods
```

### Docker Commands
```bash
# Build image
docker build -t messaging-app:latest .

# Run container
docker run -p 8000:8000 messaging-app:latest

# List containers
docker ps

# View logs
docker logs <container-id>
```

---

## 📖 Learning Resources

### Python Advanced Topics
- [Python Generators](https://docs.python.org/3/howto/functional.html#generators)
- [Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Async Programming](https://docs.python.org/3/library/asyncio.html)

### Django Framework
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Middleware](https://docs.djangoproject.com/en/stable/topics/http/middleware/)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)

### Kubernetes & DevOps
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Minikube Setup](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🎯 Key Takeaways

This repository demonstrates mastery of:

1. **Memory Efficiency** - Generators for large-scale data processing
2. **Code Reusability** - Decorators for function enhancement
3. **Concurrency** - Async/await for non-blocking operations
4. **Middleware Patterns** - Request/response pipelines
5. **Event-Driven Architecture** - Django ORM signals
6. **Container Orchestration** - Kubernetes deployment strategies
7. **DevOps Practices** - CI/CD, scaling, zero-downtime deployments
8. **Testing Strategies** - Unit and integration tests

---

## 🤝 Contributing

This repository is part of the **ALX Backend Pro-Development** curriculum. While primarily for learning, contributions and feedback are welcome!

```bash
# Fork the repository
# Create your feature branch
git checkout -b feature/AmazingFeature

# Commit your changes
git commit -m 'Add some AmazingFeature'

# Push to the branch
git push origin feature/AmazingFeature

# Open a Pull Request
```

---

## 📄 License

This project is part of the **ALX Backend Web Pro-Development Curriculum**.

© 2025 ALX Africa. All rights reserved.

---

## 👨‍💻 Author

**Thubelihle Dlamini (Dwaynemaster007)**

---

<div align="center">

### 💜 Engineered with Excellence by [Dwaynemaster007](https://github.com/Dwaynemaster007) 💜

*Building scalable backend systems, one line at a time* 🚀✨

[![GitHub](https://img.shields.io/badge/GitHub-Dwaynemaster007-181717?style=for-the-badge&logo=github)](https://github.com/Dwaynemaster007)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/dwaynemaster007)

---

**Tags:** `python` · `django` · `kubernetes` · `docker` · `generators` · `decorators` · `async-programming` · `middleware` · `orm-signals` · `container-orchestration` · `devops` · `backend-development` · `alx-backend` · `microservices` · `scalability`

</div>