DROP TABLE IF EXISTS monitoring_data;
CREATE TABLE monitoring_data (
    time TIMESTAMP PRIMARY KEY,
    key VARCHAR,
    value FLOAT
);