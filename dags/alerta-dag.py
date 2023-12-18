from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import pandas as pd

# Configura las variables de Airflow necesarias (reemplaza con tus propios valores)
smtp_server = Variable.get("smtp_server", default_var="smtp.gmail.com")
smtp_port = Variable.get("smtp_port", default_var="587")
sender_email = Variable.get("sender_email", default_var="tu_correo@gmail.com")
sender_password = Variable.get("sender_password", default_var="tu_contraseña")
receiver_email = Variable.get("receiver_email", default_var="correo_destinatario@gmail.com")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def enviar_alertas(**kwargs):
    """
    Función para enviar alertas por correo electrónico basadas en los datos actuales.
    """
    # Agrega aquí la lógica de alerta basada en tu script principal
    from scripts.Main import obtener_configuracion, obtener_datos_historicos, enviar_alerta

    config = obtener_configuracion()
    df_stock_data_staging, _, _ = obtener_datos_historicos(config)

    # Enviar alertas por correo electrónico
    alertas_config = eval(config['alertas']['lista'])
    for symbol, threshold in alertas_config:
        data_for_symbol = df_stock_data_staging[df_stock_data_staging['Symbol'] == symbol]
        today_high_value = data_for_symbol[data_for_symbol['Date'] == pd.to_datetime('today')]['High'].values

        if len(today_high_value) > 0:
            enviar_alerta(symbol, threshold, today_high_value[0])

# Configura el DAG
dag = DAG(
    'alerta_dag',
    default_args=default_args,
    description='DAG para enviar alertas por correo electrónico',
    schedule_interval=timedelta(days=1),  # Ejecutar diariamente
)

# Tareas del DAG
inicio = DummyOperator(task_id='inicio', dag=dag)

enviar_alertas_task = PythonOperator(
    task_id='enviar_alertas',
    python_callable=enviar_alertas,
    provide_context=True,
    dag=dag,
)

# Definir el orden de las tareas
inicio >> enviar_alertas_task
