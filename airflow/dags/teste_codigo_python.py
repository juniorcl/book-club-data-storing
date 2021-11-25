from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

i = 0

def somando():
    
    i = 0
    i = i + 111
    print(f'Primeira função. O valor encontrado de i é {i}')
    return i

def somando_2():

    i = i + 222
    print(f'Segunda função. O valor encontrado de i é {i}')
    return i


args = {
    'owner': 'teste',
    'start_date': days_ago(2)
}

with DAG(
    dag_id='fluxo_algoritmo_python',
    default_args=args,
    schedule_interval='* * * * *'
) as dag:

    sum_1 = PythonOperator(
        task_id='sumando',
        python_callable=somando)

    sum_2 = PythonOperator(
        task_id='sumando_2',
        python_callable=somando_2)

    sum_1 >> sum_2