from datetime import timedelta
from pprint import pprint

import pendulum
from airflow.decorators import dag, task

default_task_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": "test@test.com",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "execution_timeout": timedelta(minutes=10),
}

@dag(
    schedule_interval="@daily",
    start_date=pendulum.datetime(2024, 8, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args,
)
def context_test_dag():
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return "Whatever you return gets printed in the logs"

    print_context()


context_test_dag()
