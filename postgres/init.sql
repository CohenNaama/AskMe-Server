DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'askdb') THEN
        CREATE DATABASE askdb;
    END IF;
END
$$;
