import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

def get_gcs_path(folder):
    bucket_name = os.getenv("BUCKET_NAME", "logi-lake")
    return f"gs://{bucket_name}/{folder}"

def get_spark_session(app_name="logi-spark-job"):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jar_path_fs = os.path.join(project_root, "spark", "gcs-connector.jar").replace("\\", "/")
    temp_dir = os.path.join(project_root, "logs", "spark-temp").replace("\\", "/")
    if not os.path.exists(jar_path_fs):
        raise FileNotFoundError(f"GCS-коннектор не найден по пути: {jar_path_fs}")
    jar_path = "file:///" + jar_path_fs
    key_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "keys/logi_key.json")
    if not os.path.isabs(key_file):
        key_file = os.path.join(project_root, key_file)
    key_file = key_file.replace("\\", "/")
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.jars", jar_path)
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.local.dir", temp_dir)
        .config("spark.hadoop.fs.gs.outputstream.upload.chunk.size", "8388608")
        .config("spark.hadoop.fs.gs.outputstream.upload.max.active.requests", "4")
        .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
        .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        .config("spark.hadoop.google.cloud.auth.service.account.enable", "true")
        .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", key_file)
        .config("spark.driver.memory", "4g")
        .getOrCreate()
    )