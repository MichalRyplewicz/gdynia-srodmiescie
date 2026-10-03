SELECT  
    TRIM(UNNEST(
        string_to_array(
            REPLACE(LOWER(dada.ground_floor_function),'_',' '),
            ','
        )
    )) AS functions, 
    COUNT(*) 
FROM dataset_gdynia_raw dada
GROUP BY functions;