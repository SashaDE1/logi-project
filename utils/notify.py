import os
import requests

def send_telegram_message(message: str):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send alert: {response.text}")

def notify_failure(context):
    task_instance = context.get('task_instance')
    dag_id = task_instance.dag_id
    task_id = task_instance.task_id
    log_url = task_instance.log_url
    
    exec_date = context.get('execution_date').strftime('%Y-%m-%d %H:%M:%S')

    message = (
        f"🚨 <b>Airflow Task Failed</b>\n\n"
        f"<b>DAG:</b> {dag_id}\n"
        f"<b>Task:</b> {task_id}\n"
        f"<b>Time:</b> {exec_date}\n\n"
        f"<a href='{log_url}'>Посмотреть логи</a>"
    )
    
    send_telegram_message(message)