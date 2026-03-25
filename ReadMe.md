# 🚀 Data Pipeline Project

## 📌 Overview

This project implements a **containerized data pipeline** using **Flask**, **FastAPI**, **PostgreSQL**, and **dlt**.

The system simulates fetching customer data from an external API, ingesting it into a database using a modern data loading approach, and exposing it through backend APIs.

---

## 🧱 Architecture

```
Flask (Mock API) → FastAPI (dlt Ingestion Service) → PostgreSQL (Database) → API Response
```

---

## ⚙️ Tech Stack

* **Flask** – Mock data API
* **FastAPI** – Backend ingestion & API service
* **PostgreSQL** – Data storage
* **SQLAlchemy** – ORM for querying
* **dlt** – Data ingestion with merge (upsert) support
* **Docker & Docker Compose** – Containerization

---

## 📁 Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── Dockerfile
    └── requirements.txt
```

---

## 🚀 Getting Started

### 🔹 Prerequisites

* Docker Desktop installed and running
* Docker Compose

---

### 🔹 Run the Project

```bash
docker compose up --build
```

---

## 🌐 Services

| Service           | URL                        |
| ----------------- | -------------------------- |
| Flask Mock Server | http://localhost:5000      |
| FastAPI Service   | http://localhost:8000      |
| FastAPI Docs      | http://localhost:8000/docs |

---

## 📡 API Endpoints

### 🔹 Flask (Mock Server)

* `GET /api/health` – Health check
* `GET /api/customers?page=1&limit=10` – Paginated customers
* `GET /api/customers/{id}` – Get single customer

---

### 🔹 FastAPI (Pipeline Service)

#### 1. Ingest Data

```http
POST /api/ingest
```

Fetches all customer data from Flask and ingests it into PostgreSQL using **dlt with merge (upsert)**.

**Response:**

```json
{
  "status": "success",
  "records_processed": 20
}
```

> Note: `records_processed` reflects the number of records processed during ingestion.

---

#### 2. Get Customers (Paginated)

```http
GET /api/customers?page=1&limit=10
```

---

#### 3. Get Single Customer

```http
GET /api/customers/{id}
```

---

## 🔁 Data Flow

1. Flask serves customer data from a JSON file
2. FastAPI fetches data using pagination
3. Data is streamed into a dlt pipeline
4. dlt performs **merge (upsert)** into PostgreSQL using `customer_id`
5. FastAPI exposes APIs to query stored data

---

## 🧪 Testing

### 🔹 Test Flask

```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```

### 🔹 Ingest Data

```bash
curl -X POST http://localhost:8000/api/ingest
```

### 🔹 Fetch from Database

```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

---

## ✅ Features

* Pagination support (Flask & FastAPI)
* Data ingestion using dlt
* Upsert logic using `merge` with primary key
* RESTful APIs
* Dockerized multi-service architecture
* Health checks for service readiness
* Type-safe ingestion (date, decimal, timestamp conversion)

---

## 🧠 Design Decisions

* Flask is used to simulate an external API source
* FastAPI is used for high-performance backend services
* dlt simplifies ingestion and handles upsert logic efficiently
* SQLAlchemy is used for querying structured data
* Docker Compose ensures consistent environment setup

---

## 📌 Future Improvements

* Add authentication & authorization
* Add logging and monitoring
* Implement async ingestion
* Add retry and failure handling
* Integrate CI/CD pipeline

---

## 👨‍💻 Author

Deepak Majhi
