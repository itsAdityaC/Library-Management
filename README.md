# Library Management System (Flask + Git + Jenkins + Docker)

A Flask web app to browse, search, add, issue and return books.
CI/CD: GitHub -> Jenkins (Build, Test) -> Docker image -> Docker container.

## Run locally
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    pytest
    python app.py          # http://localhost:5000

## Run with Docker
    docker build -t library-app .
    docker run -d --name library-container -p 5000:5000 library-app

## Endpoints
- `/`           main page (search, add, issue, return)
- `/api/books`  JSON list of books
- `/health`     health check

## Pipeline stages (Jenkinsfile)
Checkout -> Build -> Test -> Docker Build -> Deploy
