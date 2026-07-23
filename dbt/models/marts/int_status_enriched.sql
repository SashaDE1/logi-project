WITH status AS(
    SELECT * FROM {{ref('stg_status')}}
),
stations AS(
    SELECT * FROM {{ref('stg_stations')}}
),
weather AS(
    SELECT * FROM {{ref('stg_weather')}}
),
enriched AS(
    SELECT
        st.station_id,
        sn.station_name,
        sn.lat,
        sn.lng,
        sn.capacity,
        st.num_bikes_available,
        st.num_docks_available,
        st.last_reported,
        w.temperature,
        w.precipitation,
        w.wind_speed,
        st.dt
    FROM status AS st
    LEFT JOIN stations AS sn
    ON st.station_id=sn.station_id
    LEFT JOIN weather AS w
    ON sn.lat=w.lat AND sn.lng=w.lng AND st.dt=w.dt
)

SELECT * FROM enriched