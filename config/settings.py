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

#--POSTGRES--
DB_USER = os.getenv("DB_USER", "logi_admin").replace('\xa0', '').strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "logi_secure_pass").replace('\xa0', '').strip()
DB_NAME = os.getenv("DB_NAME", "logi_db").replace('\xa0', '').strip()
DB_PORT = os.getenv("DB_PORT", "5432").replace('\xa0', '').strip()
DB_HOST = "postgres-logi"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GCP_KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "keys/logi_key.json")
if not os.path.isabs(GCP_KEY_PATH):
    GCP_KEY_PATH = os.path.join(PROJECT_ROOT, GCP_KEY_PATH).replace("\\", "/")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_KEY_PATH