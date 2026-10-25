CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS audit.schema_migrations (
    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_name   text        NOT NULL UNIQUE,
    checksum    text        NOT NULL,
    applied_at  timestamptz NOT NULL DEFAULT now()
);