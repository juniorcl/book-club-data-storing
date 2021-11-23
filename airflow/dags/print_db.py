import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

args = {
    'owner': 'teste',
    'start_date': airflow.utils.dates.days_ago(2)
}

with DAG(
    dag_id='fluxo_simples',
    default_args=args,
    schedule_interval=timedelta(days=1),
    dagrun_timeout=timedelta(minutes=60)
) as dag:

    # (...)
    # Depois da preparação da DAG
    # 1. Imprime a data na saída padrão
    task1 = BashOperator(
        task_id='print_date',
        bash_command='date'
    )

    # 2. Faz uma sleep de 5 segundos.
    # Dando errado tente em no máximo 3 vezes
    task2 = BashOperator(
        task_id='sleep',
        bash_command='sleep 5'
    )

    # 3. Salve a data em um arquivo texto
    task3 = BashOperator(
        task_id='list_db',
        bash_command='ls /opt/airflow/db'
    )

    task4 = BashOperator(
        task_id='reate_file',
        bash_command='touch /opt/airflow/db/sss.dat'
    )

    task1 >> task2 >> task3 >> task4