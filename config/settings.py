import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID=os.getenv("GCP_ID")
BUCKET_NAME="logi-lake"
REGION="EU"

BQ_DATASET_RAW="raw"
BQ_DATASET_STAGING="staging"
BQ_DATASET_MARTS="marts"

BRONZE_STATUS_PATH="bronze/status"
BRONZE_STATIONS_PATH="bronze/stations"
BRONZE_WEATHER_PATH="bronze/weather"
BRONZE_TRIPS_PATH="bronze/trips"

SILVER_STATUS_PATH="silver/status"
SILVER_STATIONS_PATH="silver/stations"
SILVER_WEATHER_PATH="silver/weather"
SILVER_TRIPS_PATH="silver/trips"