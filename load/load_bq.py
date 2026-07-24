import os
import config.settings
from dotenv import load_dotenv
from google.cloud import bigquery
from spark.config import get_gcs_path

load_dotenv()

def get_bq_client():
    return bigquery.Client()

def get_table_id(table_name):
    project_id=os.getenv("GCP_ID")
    return f"{project_id}.staging.{table_name}"

def load_parquet_to_bq(client, folder_name, table_name, is_partitioned=True):
    gcs_uri=f"{get_gcs_path('silver/'+folder_name)}/*"
    table_id=get_table_id(table_name)

    job_config=bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    if is_partitioned:
        hive_opts=bigquery.HivePartitioningOptions()
        hive_opts.mode="AUTO"
        hive_opts.source_uri_prefix=get_gcs_path(f"silver/{folder_name}")
        job_config.hive_partitioning=hive_opts
    
    print(f"{gcs_uri} в {table_id}")
    load_job=client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
    load_job.result()
    print(f"количество строк загружено: {load_job.output_rows}")

def load_all_to_staging():
    client = get_bq_client()

    load_parquet_to_bq(client, "stations", "stg_stations_raw", is_partitioned=False)
    load_parquet_to_bq(client, "status", "stg_status_raw", is_partitioned=True)
    load_parquet_to_bq(client, "weather", "stg_weather_raw", is_partitioned=True)
    load_parquet_to_bq(client, "trips", "stg_trips_raw", is_partitioned=True)

if __name__=='__main__':
    load_all_to_staging()