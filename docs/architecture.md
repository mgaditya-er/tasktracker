# TaskTracker Backend Architecture

## Overview

TaskTracker is a REST API backend application built using FastAPI and PostgreSQL.

The application provides APIs for:

* User Management
* Task Management
* Health Monitoring
* Readiness Checks

The architecture follows a layered design to ensure maintainability, scalability, and testability.

---

# High Level Architecture

```text
                    +------------------+
                    |     Client       |
                    | Postman / UI App |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |    FastAPI API   |
                    +--------+---------+
                             |
        +--------------------+--------------------+
        |                                         |
        v                                         v
+------------------+                 +------------------+
|   Request Layer  |                 | Middleware Layer |
|    Routers       |                 |  Request ID      |
+--------+---------+                 +--------+---------+
         |                                     |
         +----------------+--------------------+
                          |
                          v
                 +------------------+
                 |  Service Layer   |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 | Database Layer   |
                 | SQLAlchemy ORM   |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 |   PostgreSQL     |
                 +------------------+
```

---

# Project Structure

```text
TaskTracker/
│
├── app/
│   ├── api/
│   │   ├── health.py
│   │   ├── ready.py
│   │   ├── users.py
│   │   └── tasks.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── startup.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── middleware/
│   │   └── request_id.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── task.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── task_service.py
│   │
│   └── main.py
│
├── tests/
├── docs/
│   └── architecture.md
│
├── requirements.txt
├── README.md
└── Makefile
```

---

# Component Description

## API Layer

Location:

```text
app/api/
```

Responsibilities:

* Receive HTTP requests
* Validate request payloads
* Call business logic
* Return API responses

Endpoints:

### User APIs

```text
POST   /users
GET    /users
GET    /users/{id}
```

### Task APIs

```text
POST   /tasks
GET    /tasks
GET    /tasks/{id}
PUT    /tasks/{id}
DELETE /tasks/{id}
```

### Monitoring APIs

```text
GET /healthz
GET /readyz
```

---

## Schema Layer

Location:

```text
app/schemas/
```

Responsibilities:

* Request validation
* Response serialization
* Input sanitization

Examples:

```python
UserCreate
UserResponse

TaskCreate
TaskUpdate
TaskResponse
```

---

## Model Layer

Location:

```text
app/models/
```

Responsibilities:

* Database table definitions
* ORM mapping

### User Table

```text
users
```

Fields:

```text
id
name
email
```

### Task Table

```text
tasks
```

Fields:

```text
id
title
description
status
owner_id
```

---

## Database Layer

Location:

```text
app/db/
```

Responsibilities:

* Database connection
* Session management
* Transaction handling

Files:

### base.py

Responsible for:

```text
SQLAlchemy Base Declaration
```

### session.py

Responsible for:

```text
Database Engine
SessionLocal
Dependency Injection
```

---

## Middleware Layer

Location:

```text
app/middleware/
```

Responsibilities:

* Request Tracking
* Request ID Generation

Example:

```text
X-Request-ID
```

Benefits:

* Easier debugging
* Log correlation
* Distributed tracing support

---

## Logging Layer

Location:

```text
app/core/logger.py
```

Responsibilities:

* Structured logging
* Error logging
* Request tracing

Example Log:

```json
{
  "timestamp": "2026-01-01T10:00:00",
  "level": "INFO",
  "message": "task created",
  "request_id": "abc123"
}
```

---

# Database Design

## Entity Relationship Diagram

```text
+---------+
|  Users  |
+---------+
| id      |
| name    |
| email   |
+----+----+
     |
     |
     | One-to-Many
     |
     v
+------------+
|   Tasks    |
+------------+
| id         |
| title      |
| description|
| status     |
| owner_id   |
+------------+
```

Relationship:

```text
One User
can own
Many Tasks
```

---

# Request Flow

## Create Task Flow

```text
Client
   |
   v
POST /tasks
   |
   v
TaskCreate Schema Validation
   |
   v
Owner Validation
   |
   v
Task Model Creation
   |
   v
Database Commit
   |
   v
Response Returned
```

---

# Error Handling

Supported Errors:

## Validation Error

```text
400 Bad Request
```

Example:

```json
{
  "detail": "Invalid task status"
}
```

---

## Resource Not Found

```text
404 Not Found
```

Example:

```json
{
  "detail": "Task not found"
}
```

---

## Duplicate Resource

```text
409 Conflict
```

Example:

```json
{
  "detail": "Email already exists"
}
```

---

# Testing Strategy

Framework:

```text
pytest
```

Coverage Areas:

* User APIs
* Task APIs
* Validation Rules
* Error Handling
* Health Checks
* Readiness Checks

Current Target:

```text
80%+
```

---

# Deployment Architecture (Future)

```text
                    Internet
                        |
                        v
               +----------------+
               | Load Balancer  |
               +-------+--------+
                       |
                       v
                Kubernetes
                       |
       +---------------+---------------+
       |                               |
       v                               v
+-------------+               +-------------+
| FastAPI Pod |               | FastAPI Pod |
+------+------+               +------+------+
       |                               |
       +---------------+---------------+
                       |
                       v
                PostgreSQL
                       |
                       v
                    Storage
```

Future Additions:

* Docker
* Kubernetes
* Alembic
* CI/CD Pipeline
* Redis Cache
* JWT Authentication
* Monitoring & Alerting

---

# Design Principles

The application follows:

* Separation of Concerns
* Dependency Injection
* Layered Architecture
* RESTful API Design
* Test-Driven Development
* Structured Logging
* Scalability First Approach
