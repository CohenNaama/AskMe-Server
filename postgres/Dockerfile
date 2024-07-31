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
