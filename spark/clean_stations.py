from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType, TimestampType
from spark.config import get_spark_session, get_gcs_path

def clean_stations():
    spark = get_spark_session("clean-stations")
    
    bronze_path = get_gcs_path("bronze/stations/*.csv")
    print(f"Чтение из: {bronze_path}")
    df_raw = spark.read.option("header", "true").csv(bronze_path)

    df_cleaned = (
        df_raw
        .withColumn("lat", F.col("lat").cast(DoubleType()))
        .withColumn("lon", F.col("lon").cast(DoubleType()))
        .withColumn("capacity", F.col("capacity").cast(IntegerType()))
        .withColumn("updated_at", F.col("updated_at").cast(TimestampType()))
        .sort(F.col("updated_at").desc())
        .dropDuplicates(["station_id"])
    )
    
    silver_path = get_gcs_path("silver/stations")
    print(f"Запись в: {silver_path}")
    df_cleaned.write.mode("overwrite").parquet(silver_path)
    
if __name__ == "__main__":
    clean_stations()