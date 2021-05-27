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
    'dbt_advanced_dag_utility_perf_test',
    default_args=default_args,
    description='A dbt wrapper for Airflow using a utility class to map the dbt DAG to Airflow tasks',
    schedule_interval=None,
)

with dag:

    start_dummy = DummyOperator(task_id='start')
    dbt_seed = DummyOperator(task_id='dbt_seed')  # changing seed to a dummy here so it won't be benchmarked
    end_dummy = DummyOperator(task_id='end')

    dag_parser = DbtDagParser(dag=dag,
                              dbt_global_cli_flags=DBT_GLOBAL_CLI_FLAGS,
                              dbt_project_dir=DBT_PROJECT_DIR,
                              dbt_profiles_dir=DBT_PROJECT_DIR,
                              dbt_target=DBT_TARGET
                              )
    dbt_run_group = dag_parser.get_dbt_run_group()
    dbt_test_group = dag_parser.get_dbt_test_group()

    start_dummy >> dbt_seed >> dbt_run_group >> dbt_test_group >> end_dummy
