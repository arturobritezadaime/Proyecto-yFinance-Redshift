from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from scripts.Main import main


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 3),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ejecucion_diaria_main',
    default_args=default_args,
    description='DAG para ejecutar el script main.py diariamente',
    schedule_interval=timedelta(days=1),
)

# Dummy operators
dummy_inicio = DummyOperator(
    task_id='dummy_inicio',
    dag=dag,
)


# Python operator para ejecutar main.py
main_task = PythonOperator(
    task_id='main',
    python_callable=main,  # Función en main.py
    provide_context=True,
    dag=dag,
)

# Define el orden de ejecución
dummy_inicio >> main_task
