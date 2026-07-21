from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
from spark.config import get_spark_session, get_gcs_path


def clean_trips():
    spark = get_spark_session("clean-trips")

    bronze_path = get_gcs_path("bronze/trips")
    print(f"Чтение trips из: {bronze_path}")
    df_raw = spark.read.option("header", "true").csv(bronze_path)

    df_cleaned_trips = (
        df_raw
        .withColumn("started_at", F.to_timestamp(F.col("started_at")))
        .withColumn("ended_at", F.to_timestamp(F.col("ended_at")))
        .withColumn("duration_sec", (F.col("ended_at").cast("long") - F.col("started_at").cast("long")))
        .withColumn("start_lat", F.col("start_lat").cast(DoubleType()))
        .withColumn("start_lng", F.col("start_lng").cast(DoubleType()))
        .withColumn("end_lat", F.col("end_lat").cast(DoubleType()))
        .withColumn("end_lng", F.col("end_lng").cast(DoubleType()))
        .withColumn("dt", F.to_date(F.col("started_at")))
        .filter(
            F.col("start_station_id").isNotNull() &
            F.col("end_station_id").isNotNull() &
            (F.col("duration_sec") > 0)
        )
        .dropDuplicates(["ride_id"])
    )

    silver_path = get_gcs_path("silver/trips")
    print(f"Запись trips в: {silver_path}")
    (
        df_cleaned_trips
        .write
        .mode("append")
        .partitionBy("dt")
        .parquet(silver_path)
    )

if __name__ == "__main__":
    clean_trips()