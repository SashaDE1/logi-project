from datetime import datetime, timedelta
from utils.notify import notify_failure
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args={
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'on_failure_callback': notify_failure,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='logi_main_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    start_date=datetime(2024, 1,1),
    catchup=False,
    tags=['logi', 'frequent'],
) as dag:
    
    sync_stations_pg=BashOperator(
        task_id='sync_stations_pg',
        bash_command='python /opt/airflow/extract/sync_stations.py'
    )

    db_stations=BashOperator(
        task_id='db_stations',
        bash_command='python /opt/airflow/extract/db_stations.py'
    )

    api_station_status=BashOperator(
        task_id='api_station_status',
        bash_command='python /opt/airflow/extract/api_station_status.py'
    )

    api_weather=BashOperator(
        task_id='api_weather',
        bash_command='python /opt/airflow/extract/api_weather.py'
    )

    clean_stations=BashOperator(
        task_id='clean_stations',
        bash_command='python /opt/airflow/spark/clean_stations.py'
    )

    clean_status=BashOperator(
        task_id='clean_status',
        bash_command='python /opt/airflow/spark/clean_status.py'
    )

    clean_weather=BashOperator(
        task_id='clean_weather',
        bash_command='python /opt/airflow/spark/clean_weather.py'
    )

    load_staging=BashOperator(
        task_id='load_staging',
        bash_command='python /opt/airflow/load/load_bq.py'
    )

    dbt_run=BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir .'
    )

    dbt_test=BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir .'
    )

    sync_stations_pg>>db_stations>>[clean_stations, api_weather]
    api_station_status>>clean_status
    api_weather>>clean_weather

    [clean_stations, clean_status, clean_weather]>>load_staging>>dbt_run>>dbt_test