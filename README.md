# Walk Service – Cloud Run Microservice

The **Walk Service** is the backend API for a **dog-walking application**, responsible for managing the full lifecycle of dog walks. In practical terms, this service is what a mobile app or web frontend would call when a dog owner requests a walk, when a walker accepts that request, and when the walk’s status changes over time.

**This microservice was developed as a project for a Cloud Computing course**, with the goal of practicing cloud-native backend design, containerization, managed deployment, and event-driven architectures on Google Cloud Platform.

Concretely, the service allows clients to:
- Create a new walk request with specific details such as owner ID, pet ID, city/location, scheduled time, and walk duration
- Assign a walker to an existing walk request
- Update and query the current status of a walk (for example: requested, assigned, completed)
- Retrieve stored walk information for display in user-facing applications

Each of these actions is exposed as a **RESTful endpoint** implemented using **FastAPI**.

The service is packaged as a Docker container and deployed on **Google Cloud Run**, allowing it to scale automatically without manual server management. For simplicity, the core CRUD logic uses in-memory storage, while a dedicated endpoint demonstrates real cloud integration by connecting to a **Google Cloud SQL (MySQL)** database through a secure Cloud SQL connector. In addition, the service publishes structured events (such as when a walk is created) to **Google Cloud Pub/Sub**, enabling other services—like notifications, analytics, or logging—to react asynchronously in an event-driven architecture.

---

## 🚀 Features

- FastAPI-based microservice  
- In-memory CRUD operations  
- Cloud SQL connection (`/test-db` endpoint)  
- Dockerized & deployable on Cloud Run  
- Auto-generated OpenAPI docs

---

## 🎥 Demo Video

![Walk Service Demo](Cloud Computing HW1.mp4)

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
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the service
```bash
uvicorn main:app --reload
```

The service will run at:
```
http://localhost:8000
```

### 4. API Docs
Open:
```
http://localhost:8000/docs
```

> **Note (Local Development):**  
> When running locally, Google Cloud services such as Pub/Sub are automatically disabled unless valid Application Default Credentials and environment variables are provided.  
> Events will be logged locally instead of being published to Pub/Sub.

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

---

## ⚡ Google Cloud Function & Event Triggering (Pub/Sub Integration)

This project includes a **Google Cloud Function** that is automatically triggered when the Walk Service publishes events to a **Pub/Sub topic**. This satisfies the requirement:  
**“Implement at least one Google Cloud Function and demonstrate triggering it via a microservice event.”**

---

### 1. Cloud Function: `walk-event-handler`

The function listens to the Pub/Sub topic **`walk-events`** and processes messages published by the Walk Service.

```python
def handle_walk_event(event, context):
    import base64
    import json

    if "data" in event:
        message_bytes = base64.b64decode(event["data"])
        message_json = json.loads(message_bytes.decode("utf-8"))
        print("Received walk event:", message_json)
    else:
        print("No event data received.")
```

### Deploy the function

```
gcloud functions deploy walk-event-handler     --region=us-central1     --runtime=python311     --trigger-topic=walk-events     --entry-point=handle_walk_event
```

---

## 2. Walk Service Publishes Events

Creating a walk triggers:

```python
publish_event("walk_created", new_walk_dict)
```

Example message:

```json
{
  "event_type": "walk_created",
  "walk": {
    "id": "uuid-string",
    "owner_id": "uuid-string",
    "walker_id": null,
    "city": "New York",
    "status": "requested",
    "scheduled_time": "2025-12-12T10:00:00Z",
    "duration_minutes": 30
  },
  "timestamp": "2025-12-12T04:34:12Z"
}
```

---

## 3. Triggering the Cloud Function

Send a POST request:

```
POST https://walk-service-XXXX.run.app/walks
Content-Type: application/json
```

Example payload:

```json
{
  "id": "11111111-1111-1111-1111-111111111111",
  "owner_id": "22222222-2222-2222-2222-222222222222",
  "pet_id": "33333333-3333-3333-3333-333333333333",
  "location": "123 Main St, New York, NY",
  "city": "New York",
  "status": "requested",
  "scheduled_time": "2025-12-12T10:00:00Z",
  "duration_minutes": 30
}
```

View function logs:

```
gcloud functions logs read walk-event-handler --region=us-central1
```

You'll see:

```
Received walk event: {...}
```
