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
├── python-generators-0x00/               # Streaming MySQL rows with generators (+ user_data.csv sample)
├── python-decorators-0x01/               # Logging, connection, transaction, retry and cache decorators
├── python-context-async-perations-0x02/  # Context managers and concurrent queries with asyncio
├── 0x03-Unittests_and_integration_tests/ # unittest, parameterized and mock
├── messaging_app/                        # Django REST messaging API (JWT) + Docker, Jenkins and Kubernetes
├── Django-Middleware-0x03/               # The messaging API with custom middleware
└── Django-signals_orm-0x04/              # Signals, custom ORM managers, threaded replies and caching
```

---

## 🚀 Quick Start

**You need:** Python 3.10+. MySQL or MariaDB for the generator project. Docker and Minikube for the deployment tasks.

```bash
git clone https://github.com/Dwaynemaster007/alx-backend-python.git
cd alx-backend-python
python3 -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
```

Each project installs and runs on its own:

| Project | Set up | Run |
| --- | --- | --- |
| Generators | `pip install mysql-connector-python`, then set `DB_USER` and `DB_PASSWORD` | `python3 -c "import seed; c=seed.connect_db(); seed.create_database(c); c=seed.connect_to_prodev(); seed.create_table(c); seed.insert_data(c, 'user_data.csv')"`, then `python3 4-stream_ages.py` |
| Decorators | `python3 setup_db.py` (creates `users.db`) | `python3 0-log_queries.py` … `4-cache_query.py` |
| Context managers & async | `pip install aiosqlite` and `python3 setup_db.py` (creates `task_database.db`) | `python3 0-databaseconnection.py`, `1-execute.py`, `3-concurrent.py` |
| Unit tests | `pip install parameterized requests` | `python3 -m unittest test_utils test_client` |
| messaging_app, Middleware, Signals | `pip install -r requirements.txt` (Signals: `pip install django djangorestframework`) | `python manage.py migrate && python manage.py runserver`; tests: `python manage.py test` |

---

## 📚 Project Modules

### 🔄 1. Python Generators (python-generators-0x00)

- `seed.py`: creates the `ALX_prodev` MySQL database and `user_data` table, then loads `user_data.csv` (ids are generated if the CSV has none)
- `0-stream_users.py`: yields one row at a time
- `1-batch_processing.py`: yields batches and keeps users over 25
- `2-lazy_paginate.py`: fetches the next page only when it's needed
- `4-stream_ages.py`: average age without loading every row into memory

### 🎨 2. Python Decorators (python-decorators-0x01)

- `log_queries`: prints each SQL query with a timestamp
- `with_db_connection`: opens and closes the connection for you
- `transactional`: commits on success, rolls back on error
- `retry_on_failure(retries, delay)`: retries transient failures
- `cache_query`: caches results by query string

### ⚡ 3. Context Managers & Async (python-context-async-perations-0x02)

- `DatabaseConnection`: a class-based context manager that closes the connection
- `ExecuteQuery`: a context manager that runs a parameterised query
- `3-concurrent.py`: runs two `aiosqlite` queries at once with `asyncio.gather`

### 💬 4. Messaging API (messaging_app/)

A Django REST Framework API for conversations and messages.

- JWT login (`/api/auth/login/`), plus register, refresh and profile endpoints
- `/api/conversations/` and nested `/api/conversations/<id>/messages/`, with pagination, filtering and search
- Only participants can see or post in a conversation, and only the sender can edit a message
- Uses SQLite locally and MySQL under `docker compose up` (copy `.env.example` to `.env` first)

### 🛡️ 5. Django Middleware (Django-Middleware-0x03)

The messaging API plus four middleware classes in `chats/middleware.py`:

| Middleware | What it does |
| --- | --- |
| `RequestLoggingMiddleware` | Writes `timestamp - User - Path` for every request to `requests.log` |
| `RestrictAccessByTimeMiddleware` | Returns 403 for `/api/` outside 9 AM to 6 PM (`CHAT_OPEN_HOUR` and `CHAT_CLOSE_HOUR`) |
| `OffensiveLanguageMiddleware` | Rate limit: 5 messages per minute per IP, then 429 |
| `RolepermissionMiddleware` | Only admin and moderator users can open `/admin/` |

### 📡 6. Django Signals, ORM & Caching (Django-signals_orm-0x04)

- `post_save`: notifies the receiver of a new message
- `pre_save`: saves the old content to `MessageHistory` when a message is edited
- `post_delete` on `User`: cleans up a deleted user's messages, notifications and history
- `Message.unread.unread_for_user(user)`: a custom manager, queried with `.only()`
- Threaded replies through `parent_message`, loaded with `select_related` and `prefetch_related`
- `cache_page(60)` on the conversation view and the message list

| Endpoint | Description |
| --- | --- |
| `GET` `POST` `/api/thread/` | Your conversations with nested replies; send a message or reply |
| `GET` `PATCH` `/api/messages/<id>/` | Edit history; edit your own message |
| `GET` `/api/messages/unread/` | Unread messages |
| `GET` `/api/conversations/<user_id>/` | Cached conversation with one user |
| `DELETE` `/api/users/delete/` | Delete your account |

---

### 🐳 7. Container Orchestration with Kubernetes (messaging_app/)

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

### 🧪 8. Unit Tests & Integration Tests (0x03-Unittests_and_integration_tests/)

**Comprehensive testing strategies for robust applications.**

#### Learning Outcomes:
✅ Write unit tests with unittest framework  
✅ Implement integration tests  
✅ Mock external dependencies  
✅ Test coverage and quality assurance

---

## 🛠️ Common Commands

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
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/thubelihledlamini)

---

**Tags:** `python` · `django` · `kubernetes` · `docker` · `generators` · `decorators` · `async-programming` · `middleware` · `orm-signals` · `container-orchestration` · `devops` · `backend-development` · `alx-backend` · `microservices` · `scalability`

</div>