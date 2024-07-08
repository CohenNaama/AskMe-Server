# AskMe-Server

AskMeAPP is a Flask-based web application that allows users to ask questions and get answers using the OpenAI API. This application is dockerized with PostgreSQL as the database and pgAdmin for database management. It includes features for a seamless user experience through a web interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [License](#License)



## Features

- Ask questions and get answers from the OpenAI API.
- Store questions and answers in a PostgreSQL database.
- Use pgAdmin for database management.
- Fully dockerized setup with Docker Compose.
- Web interface for a pleasant user experience.
- Database migrations with Alembic.

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CohenNaama/AskMe-Server.git
   cd AskMeAPP
   
2. **Create a .env file in the root directory with the following content:**

~~~~
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost/askdb
OPENAI_API_KEY=your_openai_api_key
POSTGRES_PASSWORD=your_postgres_password
PGADMIN_DEFAULT_EMAIL=your_email@example.com
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
~~~~

3. **Ensure all your dependencies are listed in requirements.txt:**
~~~~
flask
flask_sqlalchemy
flask_migrate
python-dotenv
openai
sqlalchemy_serializer
psycopg2-binary
pytest
pytest-mock
~~~~

## Running the Application 
### Build and Run with Docker Compose 
1. Build the Docker containers:

~~~~
`docker-compose build`
~~~~

2. Run the Docker containers:

~~~~
`docker-compose up`
~~~~

This command will start three containers:

* db: PostgreSQL database
* web: Flask application
* pgadmin: pgAdmin for managing the PostgreSQL database
3. Access the application:

* Flask app: http://localhost:5000

* pgAdmin: http://localhost:8080

  * Login to pgAdmin using the credentials specified in your .env file.
  * Add a new server connection in pgAdmin to access the PostgreSQL database:
  
    * Host: db
    * Port: 5432
    * Username: postgres
    * Password: your_postgres_password
    * Database: askdb
    
## Testing 
### Running Tests 

To run tests within the Docker container, use:

~~~~
`docker-compose run web pytest`
~~~~

This command will execute all tests in your tests directory.

## Configuration ##
### Dockerfile ###
* Flask Application Dockerfile:
    
~~~~
# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disc and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy project
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the Flask application
CMD ["/wait-for-it.sh", "db:5432", "--", "flask", "run", "--host=0.0.0.0"] 
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
~~~~

## Docker Compose File ##
* docker-compose.yml:

~~~~
version: '3.8'

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: askdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: flask run --host=0.0.0.0
    environment:
      FLASK_ENV: development
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/askdb
      SECRET_KEY: ${SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "5000:5000"
    depends_on:
      - db

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "8080:80"
    depends_on:
      - db

volumes:
  postgres_data:
~~~~

# API Endpoints #
### /ask ###
### POST /ask ###
Description: Ask a question and get an answer from the OpenAI API.
Request Body: { "question": "What is the capital of Israel?"}
Response Body: { "id": 1, "question": "What is the capital of Israel?", "answer": "The capital of Israel is Jerusalem.", "created_at": "2024-07-08T10:00:00Z"}


# License
This project is licensed under the MIT License. See the LICENSE file for details.