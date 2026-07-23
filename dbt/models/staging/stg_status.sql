WITH source AS(
    SELECT * FROM {{source('staging', 'stg_status_raw')}}
), renamed AS(
    SELECT
        station_id,
        num_bikes_available,
        num_docks_available,
        last_reported,
        dt
    FROM source
)

SELECT * FROM renamed