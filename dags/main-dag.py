from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from scripts.Main import main

def install_xlsxwriter():
    import subprocess
    subprocess.run(["pip", "install", "xlsxwriter"])

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 3),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag',
    default_args=default_args,
    description='DAG con main.py',
    schedule_interval=timedelta(days=1),  # Ajusta según tus necesidades, actualmente dia=1
)

# Dummy operators
dummy_inicio = DummyOperator(
    task_id='dummy_inicio',
    dag=dag,
)

dummy_fin = DummyOperator(
    task_id='dummy_fin',
    dag=dag,
)

# Python operator para instalar xlsxwriter
install_xlsxwriter_task = PythonOperator(
    task_id='install_xlsxwriter',
    python_callable=install_xlsxwriter,
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
dummy_inicio >> install_xlsxwriter_task >> main_task >> dummy_fin
