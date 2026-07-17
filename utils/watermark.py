import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "logi_admin"),
        password=os.getenv("DB_PASSWORD", "logi_secure_pass"),
        dbname=os.getenv("DB_NAME", "logi_db")
    )

def get_watermark(table_name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT last_load_time FROM etl_watermark WHERE table_name = %s;",
                (table_name,)
            )
            result = cur.fetchone()
            return result[0] if result else None
        
def update_watermark(table_name, new_time):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO etl_watermark (table_name, last_load_time)
                VALUES (%s, %s)
                ON CONFLICT (table_name)
                DO UPDATE SET last_load_time = EXCLUDED.last_load_time;
                """,
                (table_name, new_time)
            )