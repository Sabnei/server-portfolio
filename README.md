# 🖥️ Portfolio Server

Centralized Data Engineering infrastructure running on a home server (Ubuntu 22.04). Hosts Apache Airflow and PostgreSQL as permanent Docker containers shared across all portfolio projects.

Each project lives in its own GitHub repository and is connected here as a **Git submodule** — independent versioning and documentation per project, single shared infrastructure.

---

## 🏗️ Architecture

```
Ubuntu Server (home laptop, 24/7)
└── Docker Engine
    ├── postgres-central   (port 5432)
    │   ├── schema: airflow_metadata   ← Airflow internal state
    │   ├── schema: crypto             ← crypto-etl-pipeline
    │   ├── schema: weather            ← weather-pipeline (coming)
    │   └── schema: ...               ← one schema per project
    │
    ├── airflow-webserver  (port 8080)
    ├── airflow-scheduler
    └── pgadmin            (port 5050)

dags/
├── shared_etl/                 ← shared DB connection module
│   ├── __init__.py
│   └── db.py                   ← get_engine() used by all projects
├── crypto-etl-pipeline/        ← git submodule
├── weather-pipeline/           ← git submodule (coming)
└── .../
```

Airflow scans the entire `dags/` folder recursively — it picks up DAGs from all submodules automatically, no restart needed.

---

## 📁 Repository Structure

```
portfolio-server/
├── dags/
│   ├── shared_etl/          ← shared connection module (part of this repo)
│   │   ├── __init__.py
│   │   └── db.py
│   └── crypto-etl-pipeline/ ← git submodule
├── sql/
│   └── init.sql             ← creates all schemas on first postgres start
├── logs/                    ← airflow task logs (gitignored)
├── plugins/                 ← airflow plugins (empty, required)
├── docker-compose.yml
├── Dockerfile               ← airflow image + project dependencies
├── requirements.txt
├── .env.example
└── .gitmodules
```

---

## 🚀 Setup (first time)

### 1. Install Docker on Ubuntu Server

```bash
chmod +x setup_server.sh && ./setup_server.sh
# Log out and back in so Docker works without sudo
```

### 2. Clone with submodules

```bash
git clone --recurse-submodules https://github.com/Sabnei/portfolio-server.git
cd portfolio-server
```

### 3. Configure environment

```bash
cp .env.example .env
nano .env    # set your passwords
```

### 4. Start everything

```bash
docker compose build
docker compose up airflow-init    # run once to initialize DB + create admin user
docker compose up -d              # start all services in background
```

### 5. Access

| Service | URL |
|---|---|
| Airflow UI | `http://SERVER_IP:8080` |
| pgAdmin | `http://SERVER_IP:5050` |
| PostgreSQL | `SERVER_IP:5432` |

Find your server IP: `ip addr show | grep "inet " | grep -v 127`

---

## ➕ Adding a New Project

```bash
# 1. Create and push the new project repo to GitHub

# 2. Add it as a submodule
cd dags/
git submodule add https://github.com/sabnei/new-pipeline.git new-pipeline
cd ..
git add . && git commit -m "feat: add new-pipeline submodule" && git push

# 3. On the server, pull the update
git pull && git submodule update --init --recursive

# 4. Add the schema to sql/init.sql (or create it from pgAdmin)
# Airflow detects the new DAG automatically — no restart needed
```

---

## 🔄 Updating a Project

When you push changes to a project repo and want the server to use the new version:

```bash
# Update one project
git submodule update --remote dags/crypto-etl-pipeline
git add dags/crypto-etl-pipeline
git commit -m "chore: update crypto-etl-pipeline" && git push

# Update all projects at once
git submodule update --remote --merge
git add . && git commit -m "chore: update all submodules" && git push
```

---

## 🛠️ Useful Commands

```bash
# View all running containers
docker ps

# Live logs from scheduler (where DAG errors show up)
docker compose logs -f airflow-scheduler

# Connect to postgres directly
docker compose exec postgres-central psql -U portfolio_admin -d portfolio

# Stop everything (data is preserved in the pg_data volume)
docker compose down

# Full reset including data
docker compose down -v
```

---

## 📦 Projects

| Project | Schema | Schedule | Repo |
|---|---|---|---|
| Crypto ETL Pipeline | `crypto` | `@hourly` | [crypto-etl-pipeline](https://github.com/sabnei/crypto-etl-pipeline) |
| Weather Pipeline | `weather` | coming | coming |

---

## 📄 License

MIT — see [LICENSE](LICENSE).
