import os
import io
import zipfile
import requests
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

TRIPS_BASE_URL = "https://s3.amazonaws.com/tripdata"

def blob_exists(bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.exists()

def upload_to_gcs(bucket_name, blob_name, data_string):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data_string, content_type="text/csv")
    print(f"gs://{bucket_name}/{blob_name}")

def process_month(ym_str):
    bucket_name = os.getenv("BUCKET_NAME", "logi-lake")
    target_blob = f"bronze/trips/{ym_str}-citibike-tripdata.csv"
    
    if blob_exists(bucket_name, target_blob):
        return

    url = f"{TRIPS_BASE_URL}/{ym_str}-citibike-tripdata.zip"
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        return

    zip_buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer) as z:
        csv_names = [f for f in z.namelist() if f.endswith(".csv") and "__MACOSX" not in f]
        if not csv_names:
            return
        with z.open(csv_names[0]) as csv_file:
            upload_to_gcs(bucket_name, target_blob, csv_file.read().decode("utf-8"))

def extract_trips():
    for ym in ["202404", "202405"]:
        process_month(ym)

if __name__ == "__main__":
    extract_trips()