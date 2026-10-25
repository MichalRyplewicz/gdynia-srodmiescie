DROP  TABLE IF EXISTS dataset_gdynia_fixed CASCADE;
CREATE TABLE dataset_gdynia_fixed(
    id  INTEGER PRIMARY KEY,
    osm_id  TEXT,
    addr_street TEXT,
    addr_number TEXT,
    ground_floor_group  TEXT,
    ground_floor_function   TEXT,
    upper_floor_group  TEXT,
    upper_floor_function    TEXT,
    number_of_storeys   INTEGER,
    is_mixed_use    BOOLEAN,
    build_year_est  INTEGER,
    arch_style  TEXT,
    condition   INTEGER,
    max_height  DOUBLE PRECISION,
    is_heritage TEXT,
    source TEXT,
    confidence INTEGER,
    date_of_checking DATE
    num_func INTEGER
);
\copy dataset_gdynia_fixed FROM 'data/processed/fixed/srodmiescie.csv' WITH(FORMAT CSV, HEADER, DELIMITER ';', ENCODING 'UTF8')

DROP  TABLE IF EXISTS dataset_gdynia_long CASCADE;
CREATE TABLE dataset_gdynia_long(
    id  INTEGER ,
    addr_street TEXT,
     ground_floor_function   TEXT

);
\copy dataset_gdynia_long FROM 'data/processed/fixed/srodmiescie_long.csv' WITH(FORMAT CSV, HEADER, DELIMITER ';', ENCODING 'UTF8')