WITH source AS(
    SELECT * FROM {{source('staging', 'stg_stations_raw')}}
), renamed AS(
    SELECT
        station_id,
        name AS station_name,
        lat,
        lon AS lng,
        capacity,
        updated_at
    FROM source
)

SELECT * FROM renamed