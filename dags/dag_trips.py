from datetime import datetime, timedelta
from utils.notify import notify_failure
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'on_failure_callback': notify_failure,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='logi_trips_dag',
    default_args=default_args,
    schedule_interval='@monthly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['logi', 'rare'],
) as dag:
    file_trips = BashOperator(
        task_id='file_trips',
        bash_command='python /opt/airflow/extract/file_trips.py'
    )

    clean_trips = BashOperator(
        task_id='clean_trips',
        bash_command='python /opt/airflow/spark/clean_trips.py'
    )

    load_trips = BashOperator(
        task_id='load_trips',
        bash_command='python /opt/airflow/load/load_bq.py'
    )

    dbt_run_trips = BashOperator(
        task_id='dbt_run_trips',
        bash_command='cd /opt/airflow/dbt && dbt run --select stg_trips fct_trips_monthly --profiles-dir .'
    )

    file_trips >> clean_trips >> load_trips >> dbt_run_trips