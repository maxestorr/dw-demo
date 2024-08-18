from datetime import timedelta
from pprint import pprint

import dlt
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
    schedule="@daily",
    start_date=pendulum.datetime(2024, 8, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args,
)
def ebird_dag():
    @task(task_id="print_the_context")
    def print_context(ds = None, **context):
        """Print the Airflow context and ds variable from the context."""
        pprint(context)
        print(ds)
        return "Whatever you return gets printed in the logs"

    # TODO: Split each dlt source into its own task in a joined task group
    #   the dlt.helpers.airflow_helper.PipelineTasksGroup did this for us
    #   but wouldn't read ds from context
    @task(task_id="load_ebird_source")
    def load_ebird_sources(ds = None):
        from include.dlt.rest_api_pipeline import ebird_source

        pipeline = dlt.pipeline(
            pipeline_name="rest_api_ebird",
            dataset_name="ebird",
            destination="duckdb",
            full_refresh=False,
        )

        load_info = pipeline.run(ebird_source(date=ds))
        print(load_info)

    print_context()
    load_ebird_sources()


ebird_dag()
