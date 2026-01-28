# Nature Diary · Personal Nature Encyclopedia (Full-stack + Distributed Skeleton)

Nature Diary is a prototype that turns everyday outdoor observations into a structured **nature encyclopedia**.
It is designed to scale from a simple demo into a production-style system with **clean APIs**, **async processing**, and **reproducible deployment**.

**What’s new in this version**
- ✅ Full-stack runnable demo (Streamlit UI + FastAPI + Postgres)
- ✅ Distributed skeleton (Redis queue + background worker)
- ✅ Async “CV inference” pipeline: entries transition **PENDING → PROCESSED** with `cv_result`
- ✅ Docker Compose for one-command local deployment
- 🎨 Figma mobile UI/UX prototype for the product vision

> Figma: https://www.figma.com/make/XF5F0VYicpI0H01BgWg7fI/Nature-Diary-App-Design?node-id=0-1&p=f&t=RODoxm7P039nnljo-0&fullscreen=1

---

## 1) Project Overview

Nature Diary targets hikers, travelers, and nature lovers:
you record a plant/animal/landscape, attach notes, and the system stores it as a structured entry.
This repo focuses on the **engineering backbone** needed to evolve toward “smart glasses + AI vision” later:

- **Streamlit UI** for quick product iteration and demo
- **FastAPI service** that exposes clean REST endpoints
- **Postgres** as the source-of-truth relational store
- **Redis** used for:
  - high-concurrency cache (hot reads)
  - message queue (job dispatch)
- **Worker** that consumes jobs asynchronously and writes results back to Postgres

---

## 2) Architecture (minimal distributed skeleton)

```text
Streamlit UI  ->  FastAPI  -> Postgres
                   |  |
                   |  +-> Redis cache (hot reads)
                   |
                   +-> Redis queue (nd:jobs) -> Worker -> Postgres (cv_result/status)
```

Why this design:

* heavy/variable-latency work (CV inference) is offloaded to a worker
* API stays responsive under load; worker scales independently

---

## 3) Quickstart (recommended): Run with Docker Compose

### Prerequisites

* Docker Desktop installed and running

### Start services

```bash
git clone [https://github.com/ZihanZhao227/nature-diary.git](https://github.com/ZihanZhao227/nature-diary.git)
cd nature-diary

docker compose -f infra/docker-compose.yml up --build
```

### Open the app

* Streamlit UI: [http://localhost:8501](http://localhost:8501)
* API docs (if enabled): [http://localhost:8000/docs](http://localhost:8000/docs)
* Health check: [http://localhost:8000/health](http://localhost:8000/health)

Stop:

```bash
docker compose -f infra/docker-compose.yml down
```

Reset DB (delete volumes):

```bash
docker compose -f infra/docker-compose.yml down -v
```

---

## 4) Demo: Async processing (PENDING → PROCESSED)

This is the key “distributed system” proof:
API enqueues a job → worker processes asynchronously → Postgres updated.

### 4.1 Create an entry (enqueue a job)

```bash
curl -s -X POST "http://localhost:8000/v1/entries" \
  -H "Content-Type: application/json" \
  -d '{"kind":"plant","title":"Test Entry","notes":"hello"}' | python3 -m json.tool
```

Copy the returned `id`, then:

### 4.2 Fetch it by id (may be PENDING at first, then PROCESSED)

```bash
ID=<paste-id-here>

curl -s "http://localhost:8000/v1/entries/$ID" | python3 -m json.tool
sleep 2
curl -s "http://localhost:8000/v1/entries/$ID" | python3 -m json.tool
```

Expected result:

* `status` becomes `PROCESSED`
* `cv_result` contains `labels` and `confidence`

---

## 5) Features (current implementation)

* ✅ **Entry management** via REST APIs

  * create / list / get by id
* ✅ **Favorites** (toggle favorite flag)
* ✅ **Async CV pipeline** (distributed skeleton)

  * PENDING → PROCESSED
  * `cv_result` persisted to Postgres
* ✅ **Redis-based primitives**

  * queue for background jobs
  * cache for hot reads (where applicable)
* ✅ **Reproducible deployment**

  * one-command local startup via Docker Compose

Planned next (roadmap):

* Replace Redis queue with Kafka (or SQS) to match production patterns
* Add real inference (open-source model forward pass) instead of stub results
* Add device-to-cloud style “remote config” endpoints (to better match IoT workflows)
* Terraform + Kubernetes manifests for cloud deployment

---

## 6) Tech Stack

* **Language:** Python 3.11
* **UI:** Streamlit
* **API:** FastAPI (Uvicorn)
* **DB:** Postgres
* **Queue/Cache:** Redis
* **Distributed worker:** Python worker consuming Redis jobs
* **Deployment:** Docker Compose (local)

---

## 7) Repository Structure (current)

```text
.
├── infra/
│   └── docker-compose.yml
├── services/
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py
│   │       ├── db.py
│   │       ├── models.py
│   │       └── schemas.py
│   ├── worker/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── worker.py
│   └── streamlit/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app.py
├── design/
│   ├── home.png
│   ├── map.png
│   ├── profile.png
│   └── setting.png
└── docs/
    └── architecture.md
```

> If you still see legacy folders from the early prototype (e.g., `backend/` or old `app/`),
> they are superseded by the `services/*` structure in this full-stack version.

---

## 8) Figma Design

Figma prototype:

* [https://www.figma.com/make/XF5F0VYicpI0H01BgWg7fI/Nature-Diary-App-Design?node-id=0-1&p=f&t=RODoxm7P039nnljo-0&fullscreen=1](https://www.figma.com/make/XF5F0VYicpI0H01BgWg7fI/Nature-Diary-App-Design?node-id=0-1&p=f&t=RODoxm7P039nnljo-0&fullscreen=1)

Key screens (optional screenshots):

* `design/home.png`
* `design/map.png`
* `design/profile.png`
* `design/setting.png`

---


