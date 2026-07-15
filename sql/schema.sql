CREATE TABLE IF NOT EXISTS stations(
    station_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    capacity INTEGER,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS etl_watermark (
    table_name VARCHAR(100) PRIMARY KEY,
    last_load_time TIMESTAMP WITH TIME ZONE NOT NULL
);

INSERT INTO etl_watermark(table_name, last_load_time)
VALUES ('stations', '1970-01-01 00:00:00+00')
ON CONFLICT (table_name) DO NOTHING;