from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType
from spark.config import get_spark_session, get_gcs_path


def clean_status():
    spark = get_spark_session("clean-status")

    bronze_path = get_gcs_path("bronze/status")
    print(f"Чтение status из: {bronze_path}")
    df_raw = spark.read.json(bronze_path)

    df_exploded = (
        df_raw.select(
            F.col("last_updated"),
            F.explode("data.stations").alias("station")
        )
        .select(
            F.col("station.station_id").alias("station_id"),
            F.col("station.num_bikes_available").cast(IntegerType()).alias("num_bikes_available"),
            F.col("station.num_docks_available").cast(IntegerType()).alias("num_docks_available"),
            F.col("station.is_installed").cast(IntegerType()).alias("is_installed"),
            F.col("station.is_renting").cast(IntegerType()).alias("is_renting"),
            F.col("station.last_reported").alias("last_reported_raw"),
            F.col("last_updated").alias("last_updated_raw")
        )
    )
    df_cleaned_status = (
        df_exploded
        .withColumn("last_reported", F.to_timestamp(F.col("last_reported_raw")))
        .withColumn("last_updated", F.to_timestamp(F.col("last_updated_raw")))
        .withColumn("dt", F.to_date(F.col("last_updated")))
        .filter(
            (F.col("is_installed") == 1) & 
            (F.col("is_renting") == 1) & 
            (F.col("last_reported_raw") > 86400)
        )
        .select(
            "station_id", "num_bikes_available", "num_docks_available", 
            "last_reported", "last_updated", "dt"
        )
    )

    silver_path = get_gcs_path("silver/status")
    print(f"Запись status в: {silver_path}")
    (
        df_cleaned_status
        .write
        .mode("append")
        .partitionBy("dt")
        .parquet(silver_path)
    )


if __name__ == "__main__":
    clean_status()