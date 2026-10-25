CREATE TABLE IF NOT EXISTS audit.load_log (
    id            integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id        uuid        NOT NULL,
    source_file   text        NOT NULL,
    source_sheet  text        NOT NULL,
    target_table  text        NOT NULL,
    file_checksum text,
    rows_read     integer     NOT NULL,
    rows_loaded   integer,
    status        text        NOT NULL CHECK (status IN ('success', 'failed')),
    error_message text,
    started_at    timestamptz NOT NULL,
    finished_at   timestamptz NOT NULL DEFAULT now()
);
