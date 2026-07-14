import io
import zipfile
import requests
from google.cloud import storage
import config.settings as settings

ZIP_URL="https://s3.amazonaws.com/tripdata/202401-citibike-tripdata.zip"

def upload_zip_to_gcs(url,bucket_name,gcs_folder):
    response=requests.get(url)
    response.raise_for_status()
    zip_buffer=io.BytesIO(response.content)

    with zipfile.ZipFile(zip_buffer) as zf:
        for file_name in zf.namelist():
            if file_name.endswith('.csv') and not file_name.startswith('__MACOSX'):
                print(file_name)
                with zf.open(file_name) as csv_file:
                    client=storage.Client()
                    bucket=client.bucket(bucket_name)
                    bucket.blob(f"{gcs_folder}/{file_name}").upload_from_file(csv_file)

if __name__=="__main__":
    upload_zip_to_gcs(ZIP_URL, settings.BUCKET_NAME, settings.BRONZE_TRIPS_PATH)