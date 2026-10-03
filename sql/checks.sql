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
    COUNT(is_heritage) * 100.0 / COUNT(*) AS is_heritage_fill,
    COUNT(source) * 100.0 / COUNT(*) AS source_fill,
    COUNT(confidence) * 100.0 / COUNT(*) AS confidence_fill,
    COUNT(date_of_checking) * 100.0 / COUNT(*) AS date_of_checking_fill

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

\copy (SELECT * FROM dataset_gdynia_fill_rate)  TO 'data/processed/checks/result_fill_rate.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_duplicate_id)  TO 'data/processed/checks/result_gdynia_duplicate_id.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_duplicate_osm_id)  TO 'data/processed/checks/result_duplicate_osm_id.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_illogical_range)  TO 'data/processed/checks/result_illogical_range.csv'  WITH (format csv, header true)
\copy (SELECT * FROM dataset_gdynia_duplicate_ground_floor_functions)  TO 'data/processed/checks/result_duplicates_floor_functions.csv'  WITH (format csv, header true)