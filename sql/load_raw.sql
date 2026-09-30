DROP  TABLE IF EXISTS dataset_gdynia_raw CASCADE;
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

CREATE VIEW dataset_gdynia_fill_rate AS
SELECT
    COUNT(id) * 100.0 / COUNT(*) AS id_fill,
    COUNT(osm_id) * 100.0 / COUNT(*) AS osm_id_fill,
    COUNT(addr_street) * 100.0 / COUNT(*) AS addr_street_fill,
    COUNT(addr_number) * 100.0 / COUNT(*) AS addr_number_fill,
    COUNT(ground_floor_group) * 100.0 / COUNT(*) AS ground_floor_group_fill,
    COUNT(ground_floor_function) * 100.0 / COUNT(*) AS ground_floor_function_fill,
    COUNT(upper_floor_group) * 100.0 / COUNT(*) AS upper_floor_group_fill,
    COUNT(upper_floor_function) * 100.0 / COUNT(*) AS upper_floor_function_fill,
    COUNT(number_of_storeys) * 100.0 / COUNT(*) AS number_of_storeys_fill,
    COUNT(is_mixed_use) * 100.0 / COUNT(*) AS is_mixed_use_fill,
    COUNT(build_year_est) * 100.0 / COUNT(*) AS build_year_est_fill,
    COUNT(arch_style) * 100.0 / COUNT(*) AS arch_style_fill,
    COUNT(condition) * 100.0 / COUNT(*) AS condition_fill,
    COUNT(max_height) * 100.0 / COUNT(*) AS max_height_fill,
    COUNT(is_heritage) * 100.0 / COUNT(*) AS is_heritage_fill
FROM dataset_gdynia_raw;


CREATE VIEW dataset_gdynia_duplicate_id AS
SELECT id, COUNT(*) as duplicates FROM dataset_gdynia_raw 
GROUP BY id
HAVING COUNT(*)>1;

CREATE VIEW dataset_gdynia_duplicate_osm_id AS
SELECT  osm_id, COUNT(*) as duplicates FROM dataset_gdynia_raw 
GROUP BY osm_id
HAVING COUNT(*)>1;

CREATE VIEW dataset_gdynia_illogical_range AS
SELECT id,build_year_est,number_of_storeys FROM dataset_gdynia_raw 
WHERE (build_year_est < 1900) OR (number_of_storeys < 1);

CREATE VIEW dataset_gdynia_duplicate_ground_floor_functions AS
SELECT
    LOWER(TRIM(ground_floor_function)) AS normalized_name,
    COUNT(DISTINCT ground_floor_function) AS variants
FROM dataset_gdynia_raw
WHERE ground_floor_function IS NOT NULL
GROUP BY LOWER(TRIM(ground_floor_function))
HAVING COUNT(DISTINCT ground_floor_function) > 1;

\copy (SELECT * FROM dataset_gdynia_fill_rate)  TO 'checkpoints/2026-09-30/output/result_fill_rate.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_duplicate_id)  TO 'checkpoints/2026-09-30/output/result_gdynia_duplicate_id.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_duplicate_osm_id)  TO 'checkpoints/2026-09-30/output/result_duplicate_osm_id.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_illogical_range)  TO 'checkpoints/2026-09-30/output/result_illogical_range.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_duplicate_ground_floor_functions)  TO 'checkpoints/2026-09-30/output/result_duplicates_floor_functions.csv'  WITH (format csv, header true)