import os
from datetime import datetime, timezone
import requests
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

STATUS_URL = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"

def upload_to_gcs(bucket_name, blob_name, data_string):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data_string, content_type="application/json")
    print(f"gs://{bucket_name}/{blob_name}")

def extract_status():
    response = requests.get(STATUS_URL, timeout=10)
    response.raise_for_status()

    bucket_name = os.getenv("BUCKET_NAME", "logi-lake")
    now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    blob_name = f"bronze/status/status_{now_str}.json"
    upload_to_gcs(bucket_name, blob_name, response.text)

if __name__ == "__main__":
    extract_status()