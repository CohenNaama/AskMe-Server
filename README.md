# AskMe-Server

**AskMeAPP is a Flask-based web application that allows users to ask natural language questions and get AI-generated answers using the OpenAI API.** 

The app features a clean and responsive web interface built with standard HTML, JavaScript, and Materialize CSS for modern styling.
It includes a PostgreSQL database with pgAdmin for management, is fully dockerized using Docker Compose, and supports automated testing and CI/CD.

🔗 **Live Demo**  
Check out the live version of AskMe here:  
👉 [askmeflaskapp.azurewebsites.net](https://askmeflaskapp.azurewebsites.net)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Python Dependencies](#-python-dependencies)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Configuration](#configuration)
- [Continuous Integration and Deployment](#continuous-integration-and-deployment)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)





## Features

- Ask questions and get answers from the OpenAI API.
- Store questions and answers in a PostgreSQL database.
- Use pgAdmin for database management.
- Fully dockerized setup with Docker Compose.
- Web interface for a pleasant user experience.
- Database migrations with Alembic.
- Automated CI/CD pipeline with GitHub Actions.

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CohenNaama/AskMe-Server.git
   cd AskMe-Server
   ```
   
2. **Create a .env file in the root directory with the following content:**

~~~~
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost/askdb
OPENAI_API_KEY=your_openai_api_key
POSTGRES_PASSWORD=your_postgres_password
PGADMIN_DEFAULT_EMAIL=your_email@example.com
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
~~~~


##  Python Dependencies

All required Python packages are listed in `requirements.txt`.  
You can install them locally (for development purposes) using:

```bash
pip install -r requirements.txt
```

### Key Dependencies
- **Flask** – Web framework

- **Flask-SQLAlchemy** – ORM for database interaction

- **Flask-Migrate** – Database migrations with Alembic

- **python-dotenv** – Manage environment variables

- **OpenAI** – Communicate with GPT API

- **psycopg2-binary** – PostgreSQL driver

- **pytest, pytest-mock** – Testing


## Running the Application 
### Build and Run with Docker Compose 
1. Build the Docker containers:

```bash
docker-compose build
```

2. Run the Docker containers:

```bash
docker-compose up
```

This command will start the following Docker containers:

- **db** – PostgreSQL database  
- **web** – Flask application  
- **pgadmin** – pgAdmin for managing the database via UI  

Once running, you can access:

-  **Flask App**: [http://localhost:5000](http://localhost:5000)  
-  **pgAdmin UI**: [http://localhost:8080](http://localhost:8080)

To set up pgAdmin:

1. Log in with the credentials from your `.env` file  
2. Add a new server connection using:  
   - **Host**: `db`  
   - **Port**: `5433`  
   - **Username**: `postgres`  
   - **Password**: `your_postgres_password`  
   - **Database**: `askdb`

    
## Testing 
### Running Tests 

To run tests within the Docker container, use:

```bash
`docker-compose run web pytest`
```

This command will execute all tests in your tests directory.

## Configuration ##
### Dockerfile ###
* Flask Application Dockerfile:
    
~~~~
# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disc and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]

~~~~

* PostgreSQL Dockerfile:

~~~~
# Dockerfile for PostgreSQL Database
FROM postgres:16

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=askdb

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Healthcheck to ensure the database is ready
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U $POSTGRES_USER || exit 1
~~~~

## Docker Compose File ##
* docker-compose.yml:

~~~~
services:
  db:
    build: ./postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: askdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: flask run --host=0.0.0.0 --port=5000
    environment:
      FLASK_ENV: development
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/askdb
      SECRET_KEY: ${SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "5000:5000"
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5000/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "8080:80"
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:80/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

volumes:
  postgres_data:

~~~~

## Continuous Integration and Deployment
### CI/CD Pipeline
This project uses GitHub Actions to automate the CI/CD pipeline. The pipeline performs the following steps:

1. Set Up Job: Initializes the CI environment on an Ubuntu runner.
2. Checkout Code: Clones the repository code into the runner.
3. Set Up Python: Installs Python 3.11.
4. Install Dependencies: Installs Python packages listed in requirements.txt.
5. Set Environment Variables: Loads secrets from GitHub into environment variables.
6. Install Docker Compose: Installs Docker Compose on the runner.
7. Run Tests: Executes unit tests using Pytest.
8. Build Docker Image: Builds Docker images for the application.
9. Docker Compose Up: Starts the application services using Docker Compose.
10. Run Alembic Migrations: Applies database migrations using Alembic.
11. Deploy to Production: Placeholder for deployment commands (to be implemented). 

To trigger the CI/CD pipeline, push changes to the master branch or create a pull request targeting master. Check the Actions tab in your GitHub repository to view the status and logs of pipeline runs.

## API Endpoints

The app exposes the following RESTful API endpoint:

### /ask ###
### POST /ask ###
Description: Ask a question and get an answer from the OpenAI API.
Request Body:
~~~~
{
 "question": "What is the capital of Israel?"
 }
~~~~
Response Body:
~~~~
{
  "id": 1, 
  "question": "What is the capital of Israel?", 
  "answer": "The capital of Israel is Jerusalem.", 
  "created_at": "2024-07-08T10:00:00Z"
  }
~~~~
---

##  Screenshots

Here's a preview of the AskMe app in action:

![AskMe Screenshot](https://github.com/user-attachments/assets/3a71c744-c84e-460e-b487-0b4807ab3f6f)


---