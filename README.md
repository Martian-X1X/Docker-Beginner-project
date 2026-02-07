# 🐳 Docker Observability Demo: Redis + Flask + Nginx

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

## 📋 Overview

This project demonstrates a **Docker Compose–based microservices architecture** with a strong focus on **resilience** and **observability** using lightweight, Docker-native tools.

The stack includes:

- **Flask (Python)** – application service
- **Redis** – key-value store dependency
- **Nginx** – reverse proxy / load balancer
- **Docker Compose** – multi-container orchestration

The project intentionally simulates dependency failures (Redis outages) to showcase:

- ✨ Graceful degradation
- 📝 Structured logging
- 🏥 Meaningful health checks
- ⚠️ Correct HTTP error handling

---

## 🏗️ Architecture

```
┌─────────┐
│ Client  │
└────┬────┘
     │
     ▼
┌──────────────┐
│ Nginx (8080) │
└──────┬───────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│ Flask App (5000)│─────▶│ Redis (6379) │
└─────────────────┘      └──────────────┘
```

- **Nginx** load-balances requests across one or more Flask containers
- **Flask** reads/writes messages from Redis
- **Redis** persists data via Docker volumes

---

## ✨ Key Features

### ✅ Application Behavior

- `/message` endpoint returns:
  - Message stored in Redis
  - Hostname of the serving container
- Redis message updates every 10 seconds via a background thread

### ✅ Resilience & Error Handling

- Redis client uses timeouts
- Redis failures are handled safely (no crashes)
- When Redis is unavailable:
  - Flask returns **HTTP 503**
  - Service stays running
  - Errors are logged clearly

### ✅ Observability

- Structured application logs (timestamps, log levels)
- Clear Redis error logs (`GET` / `SET` failures)
- Health checks reflect real dependency health
- Easy failure injection (`docker compose stop redis`)

### ✅ Docker Best Practices

- Multi-container setup with Docker Compose
- Named volumes for Redis persistence
- Environment variables for configuration
- Clean rebuild & redeploy workflow

---

## 📁 Project Structure

```
Docker-Beginner-project/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── .env
├── nginx/
│   └── nginx.conf
├── backups/
│   └── redis-backup.tar (optional)
└── README.md
```

---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd Docker-Beginner-project
```

### 2️⃣ Build the Flask image

```bash
docker build -t abdul-python-app:v9 .
```

### 3️⃣ Start all services

```bash
docker compose up -d
```

### 4️⃣ Verify services

```bash
docker compose ps
curl http://localhost:8080/message
```

**Expected response:**

```json
{
  "message": "Hello Martian from Redis + Flask!!! (timestamp)",
  "served_by": "container-id"
}
```

---

## 🔥 Failure Simulation (Observability Demo)

### Stop Redis

```bash
docker compose stop redis
```

### Call the API again

```bash
curl http://localhost:8080/message
```

**Expected response:**

```json
{
  "error": "Service temporarily unavailable",
  "served_by": "container-id"
}
```

- **HTTP status:** 503
- Flask remains healthy
- Errors appear in logs

### View logs

```bash
docker compose logs -f app
```

---

## 📈 Scaling the Application (Optional)

Scale Flask instances to 3:

```bash
docker compose up -d --scale app=3
```

Nginx will automatically load-balance requests across multiple Flask instances.

---

## 💾 Redis Data Persistence

### Backup Redis data

```bash
docker run --rm \
  -v Docker-Beginner-project_redis-data:/data \
  -v ${PWD}/backups:/backup \
  busybox tar cvf /backup/redis-backup.tar /data
```

### Restore Redis data

```bash
docker run --rm \
  -v Docker-Beginner-project_redis-data:/data \
  -v ${PWD}/backups:/backup \
  busybox tar xvf /backup/redis-backup.tar -C /
```

---

## ⚙️ Environment Variables

```env
REDIS_HOST=redis
REDIS_PORT=6379
MESSAGE=Hello Martian from Redis + Flask!!!
```

---

## 📌 Notes

- Flask runs using the **development server** (not production-ready).
- For production deployments, use **Gunicorn** or another WSGI server.
- This project is intentionally simple and Docker-native to focus on observability fundamentals before introducing heavier tooling (Prometheus, Grafana, OpenTelemetry).

---

## 🔮 Next Improvements (Planned)

- [ ] `/metrics` endpoint (Prometheus)
- [ ] Request & error counters
- [ ] Redis latency metrics
- [ ] Grafana dashboards
- [ ] Production-ready WSGI server (Gunicorn)
- [ ] Container health checks
- [ ] Automated testing

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author

**Abdullah Matin**

- GitHub: [@Martian-X1X](https://github.com/Martian-X1X)
- LinkedIn: [Abdullah Matin](https://www.linkedin.com/in/abdullahmatin6920/)

---

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

<p align="center">Made with ❤️ and 🐳</p>
