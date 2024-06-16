"""
## Dummy JSON Example
"""

import json
from airflow.decorators import dag, task
import duckdb
from pendulum import datetime
import requests


# Define the basic parameters of the DAG, like schedule and start_date
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["example"],
)
def dummy_json():
    # Define tasks
    @task
    def extract_dummy_json(endpoint: str) -> dict:
        """
        get all users.
        """
        r = requests.get(f'https://dummyjson.com/{endpoint}')
        return r.json()

    @task
    def save_dummy_json(json_data, file_name: str) -> None:
        "load users to file."
        with open(f'include/data/{file_name}.json', 'w') as f:
            json.dump(json_data, f, indent=4)

    endpoints = ['users', 'posts']
    result_1 = save_dummy_json.expand(
        json_data = extract_dummy_json.expand(endpoint=endpoints),
        file_name = endpoints
    )

    # todo: move loading to its own DAG
    # todo: change load scripts to use same expand method as above
    # todo: create dbt dags to transform data

    # # dbt doesn't handle E&L so best to do this in Airflow or using some other framework
    @task
    def load_users():
        """Load users.json into raw schema in DuckDB"""
        conn = duckdb.connect("include/data/datawarehouse.db")
        conn.sql(
            f"""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE OR REPLACE TABLE raw.dummy__users AS
            SELECT unnest(users, recursive := true)
            FROM 'include/data/users.json';
            """
        )

    @task
    def load_posts():
        """Load users.json into raw schema in DuckDB"""
        conn = duckdb.connect("include/data/datawarehouse.db")
        conn.sql(
            f"""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE OR REPLACE TABLE raw.dummy__posts AS
            SELECT unnest(posts, recursive := true)
            FROM 'include/data/posts.json';
            """
        )
    
    result_1 >> load_users() >> load_posts()

# Instantiate the DAG
dummy_json()
