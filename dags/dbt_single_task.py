from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.task_group import TaskGroup
from include.dbt_dag_parser import DbtDagParser

DBT_PROJECT_DIR = '/usr/local/airflow/dbt'
# DBT_PROJECT_DIR = '/Users/sam/code/airflow-dbt-demo/dbt'
DBT_GLOBAL_CLI_FLAGS = '--no-write-json'
DBT_TARGET = 'dev'
DBT_TAG = 'tag_staging'

default_args = {
    'owner': 'astronomer',
    'depends_on_past': False,
    'start_date': datetime(2020, 12, 23),
    'email': ['noreply@astronomer.io'],
    'email_on_failure': False
}

dag = DAG(
    'dbt_singletask',
    default_args=default_args,
    description='A dbt wrapper for Airflow using a utility class to map the dbt DAG to Airflow tasks',
    schedule_interval=None,
)

with dag:

    start_dummy = DummyOperator(task_id='start')
    dbt_seed = DummyOperator(task_id='dbt_seed')
    # We're using the dbt seed command here to populate the database for the purpose of this demo
    # dbt_seed = BashOperator(
    #     task_id='dbt_seed',
    #     bash_command=f'dbt {DBT_GLOBAL_CLI_FLAGS} seed --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}'
    # )
    end_dummy = DummyOperator(task_id='end')

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'\
        dbt {DBT_GLOBAL_CLI_FLAGS} run --target {DBT_TARGET} \
        --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}',
    )
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'\
        dbt {DBT_GLOBAL_CLI_FLAGS} test --target {DBT_TARGET} \
        --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}',
    )

    start_dummy >> dbt_seed >> dbt_run >> dbt_test >> end_dummy
