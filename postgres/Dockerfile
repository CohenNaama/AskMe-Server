# Dockerfile for PostgreSQL Database
FROM postgres:16

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=askdb

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/
