WITH source AS(
    SELECT * FROM {{ref('stg_trips')}}
), monthly_agg AS(
    SELECT
        start_station_name,
        EXTRACT(year FROM started_at) AS trip_year,
        EXTRACT(month FROM started_at) AS trip_month,
        COUNT(ride_id) AS total_trips,
        ROUND(AVG(duration_sec)/60, 2) AS avg_duration_minutes,
        SUM(CASE WHEN member_casual='member' THEN 1 ELSE 0 END) AS member_trips,
        SUM(CASE WHEN member_casual='casual' THEN 1 ELSE 0 END) AS casual_trips
    FROM source
    GROUP BY 1,2,3
)

SELECT * FROM monthly_agg