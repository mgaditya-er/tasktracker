# TaskTracker Backend

TaskTracker is a FastAPI-based backend application for managing users and tasks.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pytest
- Docker (Upcoming)
- Kubernetes (Upcoming)

---

## Features

### Users

- Create User
- Get All Users
- Get User By ID
- Duplicate Email Validation

### Tasks

- Create Task
- Get All Tasks
- Get Task By ID
- Update Task
- Delete Task
- Owner Validation
- Status Validation

### Health Checks

- /healthz
- /readyz

---

## Project Structure

```text
app/
├── api/
├── core/
├── db/
├── middleware/
├── models/
├── schemas/
└── services/

tests/
docs/