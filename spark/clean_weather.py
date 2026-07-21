from pyspark.sql import functions as F
from spark.config import get_spark_session, get_gcs_path

def clean_weather():
    spark=get_spark_session("clean-weather")

    bronze_path=get_gcs_path("bronze/weather")
    df_raw=spark.read.json(bronze_path)

    df_cleaned_weather=(
        df_raw.select(
            F.col("latitude"),
            F.col("longitude"),
            F.col("current.temperature_2m").alias("temperature"),
            F.col("current.precipitation").alias("precipitation"),
            F.col("current.wind_speed_10m").alias("wind_speed"),
            F.to_timestamp(F.col("current.time")).alias("observation_time"),
        )
        .withColumn("dt", F.to_date(F.col("observation_time")))
        .dropDuplicates(["observation_time", "latitude", "longitude"])
    )
    silver_path=get_gcs_path("silver/weather")
    (
        df_cleaned_weather
        .write
        .mode("append")
        .partitionBy("dt")
        .parquet(silver_path)
    )
    print("End")

if __name__=="__main__":
    clean_weather()