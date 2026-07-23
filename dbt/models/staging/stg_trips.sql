WITH source AS(
    SELECT * FROM {{source('staging', 'stg_trips_raw')}}
), renamed AS(
    SELECT
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        start_station_id,
        start_station_name,
        end_station_id,
        end_station_name,
        member_casual,
        duration_sec,
        dt
    FROM source
)

SELECT * FROM renamed