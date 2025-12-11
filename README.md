# Walk Service – Cloud Run Microservice

This repository contains the **Walk Service**, a FastAPI microservice for managing dog-walk requests, assignments, and event logs.
The service is fully deployed on **Google Cloud Run** and connected to a **Google Cloud SQL (MySQL)** database.

---

## 🚀 Features

- FastAPI-based microservice  
- In-memory CRUD operations  
- Cloud SQL connection (`/test-db` endpoint)  
- Dockerized & deployable on Cloud Run  
- Auto-generated OpenAPI docs

---

## 📁 Project Structure

```
.
├── Dockerfile
├── main.py
├── models/
├── services/
├── middleware/
├── framework/
├── resources/
├── utils/
│   └── db.py
├── requirements.txt
└── .gcloudignore
```

---

## 🐍 Running Locally

### 1. Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Start the service
```
uvicorn main:app --reload --port 8000
```

### 4. API Docs
Open:
```
http://localhost:8000/docs
```

---

## 🗄️ Cloud SQL Connection

Database credentials come from environment variables:

```
DB_USER
DB_PASS
DB_NAME
INSTANCE_CONNECTION_NAME
```

### Test endpoint
```
/test-db
```

If successful, you'll see MySQL server time.

---

## ☁️ Deploy to Cloud Run

### Build & push image
```
gcloud builds submit   --tag us-central1-docker.pkg.dev/PROJECT_ID/repo/walk-service
```

### Deploy
```
gcloud run deploy walk-service   --image us-central1-docker.pkg.dev/PROJECT_ID/repo/walk-service   --region us-central1   --platform managed   --allow-unauthenticated   --add-cloudsql-instances PROJECT_ID:us-central1:INSTANCE_NAME   --set-env-vars INSTANCE_CONNECTION_NAME=PROJECT_ID:us-central1:INSTANCE_NAME   --set-env-vars DB_USER=...   --set-env-vars DB_PASS=...   --set-env-vars DB_NAME=...
```

Service URL example:
```
https://walk-service-XXXX.us-central1.run.app
```

---

## 📘 API Documentation
Open:
```
/docs
```