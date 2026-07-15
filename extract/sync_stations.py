import json
import requests
import pandas as pd
from sqlalchemy import create_engine,text
import config.settings as settings

STATIONS_URL="https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json"

def sync_stations_to_pg():
    engine = create_engine(settings.DB_URL, connect_args={"client_encoding": "utf8"})
    with engine.connect() as conn:
        watermark=conn.execute(text("SELECT last_load_time FROM etl_watermark WHERE table_name='stations';")).scalar()
        print(f"Текущий watermark: {watermark}")
    
    response=requests.get(STATIONS_URL)
    response.raise_for_status()
    data=response.json()
    stations_list=data['data']['stations']
    df=pd.DataFrame(stations_list)
    df=df[['station_id', 'name', 'lat', 'lon', 'capacity']]
    df.to_sql('stations_temp', engine, if_exists='replace', index=False)

    with engine.begin() as conn:
        conn.execute(text("""
INSERT INTO stations (station_id, name, lat, lon, capacity, updated_at)
SELECT station_id, name, lat, lon, capacity, CURRENT_TIMESTAMP FROM stations_temp
ON CONFLICT (station_id) DO UPDATE SET
    name = EXCLUDED.name,
    lat = EXCLUDED.lat,
    lon = EXCLUDED.lon,
    capacity = EXCLUDED.capacity,
    updated_at = CURRENT_TIMESTAMP;

UPDATE etl_watermark SET last_load_time = CURRENT_TIMESTAMP WHERE table_name = 'stations';
DROP TABLE stations_temp;"""))
        
if __name__=="__main__":
    sync_stations_to_pg()