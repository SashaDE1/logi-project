## 1. GBFS station_status (API -> Bronze -> Silver status)
- `station_id` (STRING) - ID станции
- `num_bikes_available` (INTEGER) - доступно велосипедов
- `num_docks_available` (INTEGER) - доступно свободных доков
- `is_renting` (INTEGER/BOOLEAN) - статус аренды
- `is_installed` (INTEGER/BOOLEAN) - статус установки
- `last_reported` (TIMESTAMP) - время обновления данных станции

## 2. GBFS station_information (API -> PostgreSQL -> Bronze -> Silver stations)
- `station_id` (STRING, PK) — уникальный ID станции
- `name` (STRING) - название станции
- `lat` (FLOAT) - широта
- `lon` (FLOAT) - долгота
- `capacity` (INTEGER) - общая вместимость

## 3. Open-Meteo Weather (API -> Bronze -> Silver weather)
- `time` (TIMESTAMP) - часовой таймстемп
- `temperature_2m` (FLOAT) - температура воздуха(C)
- `precipitation` (FLOAT) - осадки(мм)
- `wind_speed_10m` (FLOAT) - скорость ветра(км/ч)

## 4. Citi Bike Trip History (S3 ZIP -> GCS -> Bronze -> Silver trips)
- `ride_id` (STRING) - уникальный ID поездки
- `rideable_type` (STRING) - тип велосипеда: classic/electric
- `started_at` (TIMESTAMP) - время начала поездки
- `ended_at` (TIMESTAMP) - время завершения поездки
- `start_station_id` (STRING) - ID станции отправления
- `end_station_id` (STRING) - ID станции прибытия
- `member_casual` (STRING) - тип абонемента: member/casual