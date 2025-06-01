# Paack Assignment API 📦

A package management API built with FastAPI using hexagonal architecture. Manages package states (`READY → IN_TRANSIT → DELIVERED`), handles concurrent updates safely, provides structured logging etc.

---

## Requirements 🛠
- Python 3.10 or 3.11
- pip package manager
- Docker Desktop (optional for containerized deployment)

---

## Installation ⚙️
- git clone https://github.com/mb-at/paack-assignment.git
- cd paack_assignment
- python -m venv venv
- Activate virtual environment:

Windows CMD:
- venv\Scripts\activate

PowerShell:
- venv\Scripts\Activate.ps1

MacOS/Linux:
- source venv/bin/activate

Install dependencies:
- pip install -r requirements.txt

---

## Running the API 🚀
Local Development (without Docker)
- uvicorn src.api.main:app --reload
- Access endpoints:
    - Health Check: http://localhost:8000/health → {"status":"ok"}
    - Swagger UI: http://localhost:8000/docs

Docker Deployment
Build image
- docker build -t paack-assignment .

Run container
- docker run -d --name paack-test -p 8000:8000 paack-assignment

Check Logs
- docker logs paack-test

---

## API Endpoints 🔌
Method	Endpoint	Description
GET	/health	Service healthcheck
GET	/packages	List all packages
PATCH	/packages/{package_id}/status	Update package status

Explore API:
- Interactive Docs: http://localhost:8000/docs
- OpenAPI Spec: openapi.yaml

---

## Running Tests 🧪
pytest -q
Test Coverage:
    - Domain services
    - Adapters implementations
    - Use cases
    - API endpoints
    - Concurrency handling