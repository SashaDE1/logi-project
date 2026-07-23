WITH source AS(
    SELECT * FROM {{source('staging', 'stg_weather_raw')}}
), renamed AS(
    SELECT
        latitude AS lat,
        longitude AS lng,
        temperature,
        precipitation,
        wind_speed,
        dt
    FROM source
)

SELECT * FROM renamed