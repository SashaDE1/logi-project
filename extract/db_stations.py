import os
import io
import csv
from datetime import datetime, timezone
from google.cloud import storage
from dotenv import load_dotenv
from utils.watermark import get_db_connection, get_watermark, update_watermark

load_dotenv()

def upload_to_gcs(bucket_name, blob_name, data_string):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data_string, content_type="text/csv")
    print(f"gs://{bucket_name}/{blob_name}")

def extract_stations():
    table_name = "stations"
    last_load = get_watermark(table_name)
    print(f"Текущая ватермарка для {table_name}: {last_load}")

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            if last_load:
                cur.execute(
                    "SELECT * FROM stations WHERE updated_at > %s ORDER BY updated_at ASC;",
                    (last_load,)
                )
            else:
                cur.execute("SELECT * FROM stations ORDER BY updated_at ASC;")
            
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

    if not rows:
        return
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(colnames)
    writer.writerows(rows)

    bucket_name = os.getenv("BUCKET_NAME", "logi-lake")
    now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    blob_name = f"bronze/stations/stations_{now_str}.csv"

    upload_to_gcs(bucket_name, blob_name, buffer.getvalue())

    updated_at_idx = colnames.index("updated_at")
    max_updated_at = max(row[updated_at_idx] for row in rows)
    update_watermark(table_name, max_updated_at)


if __name__ == "__main__":
    extract_stations()