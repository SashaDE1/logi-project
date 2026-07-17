import os
from datetime import datetime, timezone
import requests
from google.cloud import storage
from dotenv import load_dotenv
from utils.watermark import get_db_connection

load_dotenv()

WEATHER_URL="https://api.open-meteo.com/v1/forecast"

def upload_to_gcs(bucket_name, blob_name, data_string):
    client=storage.Client()
    bucket=client.bucket(bucket_name)
    blob=bucket.blob(blob_name)
    blob.upload_from_string(data_string, content_type="application/json")
    print(f"gs://{bucket_name}/{blob_name}")

def get_center_coordinates():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(lat), AVG(lon) FROM stations WHERE lat IS NOT NULL;")
            res=cur.fetchone()
            return (res[0], res[1]) if res and res[0] else (40.7128, -74.0060)
    
def extract_weather():
    lat, lon = get_center_coordinates()
    params={
        "latitude": float(lat),
        "longitude": float(lon),
        "current":["temperature_2m", "precipitation", "wind_speed_10m"]
    }

    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()

    bucket_name = os.getenv("BUCKET_NAME", "logi-lake")
    now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    blob_name = f"bronze/weather/weather_{now_str}.json"
    upload_to_gcs(bucket_name, blob_name, response.text)

if __name__ == "__main__":
    extract_weather()