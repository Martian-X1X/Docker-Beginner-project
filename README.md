# Docker Demo: Redis + Flask + Nginx Microservices

## Overview

This project demonstrates a multi-container Docker setup using:

- Flask (Python web service)
- Redis (key-value store)
- Nginx (reverse proxy / load balancer)
- Docker Compose (multi-container orchestration)

Features:

- `/message` endpoint in Flask returns a message with the serving container.
- Redis stores messages updated every 10 seconds.
- Nginx load balances multiple Flask instances.
- Docker volumes provide persistence for Redis data.
- Logs provide observability of container actions.

---

## Project Structure

docker-demo/
├─ app.py
├─ Dockerfile
├─ docker-compose.yml
├─ .env
├─ nginx/
│ └─ nginx.conf
└─ backups/
└─ redis-backup.tar (optional)


---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd docker-demo
2. Build the Flask Docker image
docker build -t abdul-python-app:v8 .
3. Start containers
docker compose up -d
4. Verify services
docker compose ps
curl http://localhost:8080/message
5. Scale Flask app instances (optional)
docker compose up -d --scale app=3
6. View logs
docker compose logs -f app
7. Backup Redis data
docker run --rm -v docker-demo_redis-data:/data -v %cd%/backups:/backup busybox tar cvf /backup/redis-backup.tar /data
8. Restore Redis data
docker run --rm -v docker-demo_redis-data:/data -v %cd%/backups:/backup busybox tar xvf /backup/redis-backup.tar -C /
9. Stop and remove all containers/volumes
docker compose down -v
Environment Variables
REDIS_HOST=redis
REDIS_PORT=6379
MESSAGE=Hello Martian from Redis + Flask!!!
Notes
Flask runs in development mode (not production-ready). For production, use Gunicorn or another WSGI server.

Logs appear in terminal; Nginx handles load balancing between app instances.

Redis data persists across container restarts via Docker volumes.


---

## **Step-by-Step Terminal Script (Windows PowerShell)**

```powershell
# 1. Navigate to project folder
cd C:\Users\Abdul\docker-demo

# 2. Build Flask Docker image
docker build -t abdul-python-app:v8 .

# 3. Start all containers
docker compose up -d

# 4. Verify services
docker compose ps
curl.exe http://localhost:8080/message

# 5. Scale Flask app (optional)
docker compose up -d --scale app=3

# 6. View logs for Flask app
docker compose logs -f app

# 7. Backup Redis data
mkdir backups
docker run --rm -v docker-demo_redis-data:/data -v ${PWD}/backups:/backup busybox tar cvf /backup/redis-backup.tar /data

# 8. Restore Redis data
docker run --rm -v docker-demo_redis-data:/data -v ${PWD}/backups:/backup busybox tar xvf /backup/redis-backup.tar -C /

# 9. Stop and clean all containers & volumes
docker compose down -v