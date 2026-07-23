WITH source AS(
    SELECT * FROM {{ref('int_status_enriched')}}
), final AS(
    SELECT
        station_id,
        station_name,
        num_bikes_available,
        num_docks_available,
        last_reported,
        temperature,
        precipitation,
        wind_speed,
        dt
    FROM source
)

SELECT * FROM final