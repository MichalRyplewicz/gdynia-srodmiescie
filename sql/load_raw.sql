DROP  TABLE IF EXISTS dataset_gdynia_raw;
CREATE TABLE dataset_gdynia_raw(
    id  INTEGER,
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
    is_heritage TEXT
);
\copy dataset_gdynia_raw FROM 'data/raw/srodmiescie_raw.csv' WITH(FORMAT CSV, HEADER, DELIMITER ';', ENCODING 'UTF8')

SELECT  addr_street, COUNT(addr_street) as record_number FROM dataset_gdynia_raw 
WHERE addr_street IS NOT NULL

GROUP BY addr_street
HAVING COUNT(addr_street) > 20
ORDER BY record_number DESC;