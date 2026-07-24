# citi-bike-pipeline

Медальон (Bronze/Silver/Gold): статус станций, справочник станций, история поездок Citi Bike + погода.

## Источники

| Источник | Тип | Частота |
|---|---|---|
| GBFS `station_status` | API | ежечасно |
| GBFS `station_information` → PostgreSQL | БД | ежечасно, watermark |
| Citi Bike trip history | файлы (CSV/ZIP) | ежемесячно |
| Open-Meteo | API | ежечасно |

## Архитектура

GCS bronze → PySpark → GCS silver (Parquet) → BigQuery staging → dbt → BigQuery marts

Два DAG:
- `dag_main` — станции, статус, погода — `@hourly`
- `dag_trips` — поездки — `@monthly`

## Стек

Python, PySpark, Airflow (Docker, LocalExecutor), dbt, PostgreSQL (Docker), GCS, BigQuery

## Структура

\`\`\`text
dags/     DAG'и
extract/  Bronze-экстракторы
spark/    Silver-очистка
load/     Silver → staging
dbt/      Gold-витрины
docker/   Dockerfile, docker-compose
sql/      DDL PostgreSQL
seed/     разовые бэкфиллы
utils/    watermark, notify
config/   settings.py
\`\`\`

## Запуск

\`\`\`bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env

docker compose --env-file .env -f docker/docker-compose.yml up -d

cd dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
\`\`\`

Airflow: `localhost:8080`

## Дашборды

- Операционный — [https://datastudio.google.com/reporting/5e3051ec-ea87-4d6f-b844-2a2c6c6bcfed]
- Погода и спрос — [ссылка]
- История баланс — [ссылка]