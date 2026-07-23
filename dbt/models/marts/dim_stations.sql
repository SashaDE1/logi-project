WITH source AS(
    SELECT * FROM {{ref('stg_stations')}}
), final AS(
    SELECT
        station_id,
        station_name,
        lat,
        lng,
        capacity,
        updated_at
    FROM source
)

SELECT * FROM final